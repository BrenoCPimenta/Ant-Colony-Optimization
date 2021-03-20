import networkx as nx
import matplotlib
import matplotlib.pyplot as plt

class Enviroment():

    def __init__(self, file_name, init_pheromone, min_pheromone):
        self.min_pheromone = min_pheromone
        #Read Data
        self.data = self.__readData(file_name)
        self.num_jobs = len(self.data)
        self.num_machines = len(self.data[0])
        #Create Graph 
        self.G, self.node_names = self.__buildGraph(init_pheromone)


    def __readData(self, file_name):
        """
        Reads file and create a first data structure.
        The structure is a Matrix:
            Line:Jobs 
            Column: Machines
            Content:time of execution.

        returns:
            The matrix.
        """        
        jobs = []
        with open("../test_instances/" + file_name,'r') as file: 
            for line in file: 
                machines = {}
                this_machine = None
                for j,value in enumerate(line.split()):
                    if j%2 != 0:
                        machines.update({this_machine : value})
                    else:
                        this_machine = value
                jobs.append(machines)

        return jobs #Named as <data> outside this method


    def __buildGraph(self, init_pheromone):
        """
        From the matrix returned on __readData() method
        creates a Direct, Weighted and FullConnected Graph 
        using networkx library.
        This library will facilitate working with edges.
        Will be added a virtual inital node (-1,-1) that connects
        to all others nodes.

        returns:
            Graph and all node names.
        """
        num_nodes = self.num_jobs*self.num_machines + 1 #All machineXjobs pair plus the initial virtual node

        #Create directed and fully connected graph, with weight zero in every edge:
        unnamed_graph = nx.complete_graph(num_nodes,  nx.DiGraph())

        #Giving proper names to the nodes:
        node_names = [(-1,-1)] #Add initial virtual node 
        for job in range(self.num_jobs):
            for machine in range(self.num_machines):
                node_names.append((job, machine))
        mapping = {i:nodename for i,nodename in enumerate(node_names)} #mapping: {0:(-1,-1), 1:(0,0), ...}
        G = nx.relabel_nodes(unnamed_graph,mapping)
        
        #Remove Edges that point to the  initial vitual node, 
        # so it only remains from initial to other nodes and not the other way arround:
        for job in range(self.num_jobs):
            for machine in range(self.num_machines):
                G.remove_edge((job, machine), (-1,-1))

        #Update Pheromone and desirability:
        for from_job in range(self.num_jobs):
            for from_machine in range(self.num_machines):
                
                #Add edge attributes (desirability/pheromone) for edges from virtual node
                execution_time = self.data[from_job][str(from_machine)]
                desirability = 1/int(execution_time)
                G[(-1,-1)][(from_job,from_machine)]['pheromone'] = init_pheromone
                G[(-1,-1)][(from_job,from_machine)]['desirability'] = desirability

                for to_job in range(self.num_jobs):
                    for to_machine in range(self.num_machines):
                        #Add edge attributes (desirability/pheromone) for edges from operational node
                        if from_job == to_job and from_machine == to_machine:
                            pass
                        else:
                            execution_time = self.data[to_job][str(to_machine)]
                            desirability = 1/int(execution_time)
                            G[(from_job,from_machine)][(to_job,to_machine)]['pheromone'] = init_pheromone
                            G[(from_job,from_machine)][(to_job,to_machine)]['desirability'] = desirability

        node_names.remove((-1,-1)) #Remove initial virtual node from names
        return G, node_names


    def getGraph(self):
        """
        Returns Graph with updated
        pheromones and node names
        """
        return self.G
    
    def getNodeNames(self):
        """
        Returns the node names
        of the Graph
        """
        return self.node_names

    def getTimeOfExecutions(self):
        """
        Returns the data readed
        with execution time of
        each node.
        """
        return self.data

    def getEdges(self):
        return [edge for edge in self.G.edges]

    
    def updatePheromone(
        self,
        evaporation_rate,
        cycle_edge_contribution): 
        """
        Simulates the pheromone evaporation
        at each edge by multipling the 
        evaporation rate to the old 
        pheromone values.
        And simulates the ants pherommone
        trails contribution when adding 
        the sum of the inverse of the 
        time of the path that passed 
        through that edge..
        """
        for edge in self.G.edges:
            from_node = edge[0]
            to_node = edge[1]
            old_pheromone = self.G[from_node][to_node]['pheromone']
            new_pheromone = cycle_edge_contribution[edge] + (evaporation_rate * old_pheromone)
            if new_pheromone > self.min_pheromone:
                self.G[from_node][to_node]['pheromone'] = new_pheromone
            else:
                self.G[from_node][to_node]['pheromone'] = self.min_pheromone    


    def calculateMakespanTime(self, path):
        """
        Calculates the optimal time (makespan)
        for the entry path to the job shop 
        scheduilling problem.

        returns:
            makespam time
        """
        #Inicialize scheduler
        machine_task_moments = [] #Represent all the tasks on their moments in wich machine
        machine_moments = [] #Represents in wich moment of time that machine is
        for i in range(self.num_machines):
            machine_task_moments.append([])
            machine_moments.append(0)

        for edge in path:
            this_job = edge[1][0]
            this_machine = edge[1][1]
            this_task_time = int(self.data[this_job][str(this_machine)])
            moment = machine_moments[this_machine]
            moment_for_task_not_found = True
            #Verify in wich moment the task can initiate
            while moment_for_task_not_found:
                foud_other_machine_with_same_task = False
                for other_machine in range(self.num_machines):
                    if other_machine == this_machine:
                        pass
                    else:
                        try:
                            if this_job == machine_task_moments[other_machine][moment]:
                                foud_other_machine_with_same_task = True
                                break
                        except:
                            pass
                
                if foud_other_machine_with_same_task == False:
                    #Stops the loop
                    moment_for_task_not_found = False
                    #fill the job time for that machine
                    for i in range(this_task_time):
                        machine_task_moments[this_machine].append(this_job)
                    machine_moments[this_machine] = this_task_time + moment + 1
                    
                else:
                    #Make the machine wait until the job is done in another machine
                    machine_task_moments[this_machine].append('-')
                    moment+=1
                    
        #--------->Uncomment next lines if you want to print the Makespan 
        #             for each schedule tested on execution:
        #for i in range(self.num_machines):
        #    print(machine_task_moments[i])

        machine_execution_lengths = []
        for i in range(self.num_machines):
            machine_execution_lengths.append(len(machine_task_moments[i]))
        return max(machine_execution_lengths)

            


    def printGraph(self):
        """
        Creates an image of the built graph

        results:
            png image: 'code/graph.png'
        """
        options = {
            'node_color': 'blue',
            'node_size': 2000,
            'width': 2.5,
            'arrowstyle': '-|>',
            'arrowsize': 20,
        }
        matplotlib.use('Agg')
        
        #Generating edge labels
        edge_labels = {}
        for from_node, to_node, edge in self.G.edges(data=True):
            desirability = round(edge['desirability'], 4)
            pheromone = round(edge['pheromone'], 3)
            weight = "(" + str(desirability) + " - " +  str(pheromone)+")"
            edge_labels.update({(from_node, to_node) : weight})

        #Generating figure    
        fig = plt.figure()        
        ax = fig.add_subplot(111)
        pos = nx.spring_layout(self.G)
        nx.draw_networkx_edge_labels(self.G,pos,edge_labels=edge_labels, font_size=7)
        nx.draw_networkx(self.G, pos, arrows=True, ax=ax, **options)
        fig.savefig('graph.png')


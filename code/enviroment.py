import networkx as nx
import matplotlib
import matplotlib.pyplot as plt

class Enviroment():

    def __init__(self, file_name, init_pheromone):
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

        return jobs #Named as data outside this method


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
    
    def getNodeNames(self)
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
        """"
        return self.data

    def evaporatePheromone(self, evaporation):
        """
        Simulates the pheromone
        evaporation at each edge of
        the graph by subtracting the 
        input value.
        """
        for from_job in range(self.num_jobs):
            for from_machine in range(self.num_machines):
                #Evaporating pheromone on edges from virtual node
                self.G[(-1,-1)][(from_job,from_machine)]['pheromone'] -= evaporation
                for to_job in range(self.num_jobs):
                    for to_machine in range(self.num_machines):
                        #Evaporating pheromone on operational edges
                        if from_job == to_job and from_machine == to_machine:
                            pass
                        else:
                            self.G[(from_job,from_machine)][(to_job,to_machine)]['pheromone'] -= evaporation
                            

    def updatePheromone(self, walk, time):
        return 22

    def calculateMakespanTime(self, path):
        #Inicialize scheduler
        machine_tasks = []
        for i in range(self.num_machines):
            machine_tasks.append([])

        for edge in path:
            
            machine_tasks



        jobs_in_execution = []
        machines_in_execution = []
        time = 0
        while path:
            for edge in path:

            


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


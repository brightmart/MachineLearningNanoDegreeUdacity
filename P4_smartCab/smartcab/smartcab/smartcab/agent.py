import random as rd
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    @staticmethod
    def zero():
        return 0
    """An agent that learns to drive in the smartcab world."""
    global GAMMA #discount rate
    GAMMA =0.5
    global runCounter
    global actionGG
    global totalReward
    totalReward=0
    global totalPenalty
    totalPenalty=0
    runCounter=0
    global alpha
    alpha=0.9#learning rate
    
    global qMatrixDict #this dict store state,action and q value. it is the key information storage for this agent.
    qMatrixDict={}
    global epsilon
    epsilon=0.1
    
    
    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'black'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        
    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
    
    @staticmethod
    def randomSelectAnAction():
        numberr=rd.randint(0,3)
        print numberr
        if numberr==0:
            action='forward'
        elif numberr==1:
            action='left'
        elif numberr==2:
            action='right'
        elif numberr==3:
            action=None
        return action
        
    @staticmethod
    def get_decay_rate(t): #Decay rate for alpha and epsilon
        return 1.0 / float(t)
        
     #given a state, find the action or q that have the biggest Q value, or update q matrix using state and action
    #Try simplify your getOrUpdateMaxQAction method. You are combining very complicated logics there. 
    #Try break your big complicated function into several small but simple functions. 
    #1.get best action; 2.get q value. 3. update q value. 4.get max possible q value.
    @staticmethod
    def getOrUpdateMaxQAction(inputs,next_waypoint,deadline,action,q,operatinType):
        print q
    #qMatrixDict structure as: {(state1):actionAndQDict1,(state2):actionAndQDict2,(state3):actionAndQDict3}
        #process input
        state=(inputs['light'],next_waypoint,inputs['oncoming'],inputs['left']) #deadline#state as Tuples---》inputs['light'],inputs['oncoming'],inputs['left'],deadline
        defaultDict={'forward':0,'left':0,'right':0,None:0}
        global qMatrixDict
        dictOfActionAndQs=qMatrixDict.get(state,defaultDict)
        if operatinType=='updateQ': 
            print action
            dictOfActionAndQs[action]=q
            global qMatrixDict
            qMatrixDict[state]=dictOfActionAndQs 
        elif operatinType=='getMaxQ' or operatinType=='getAction': #get max q for the given state(need to iterate dict)
            if dictOfActionAndQs==defaultDict:
                if operatinType=='getMaxQ':
                    return 0
                else:#get best possible action
                    return LearningAgent.randomSelectAnAction()
            else:
                qValueMax=-100
                actionBest=None
                actionBestList=[]
                for actionTemp in dictOfActionAndQs: #{'right': 2, 'left': 3,'forward':0}
                    qValue=dictOfActionAndQs[actionTemp]
                    if qValue>qValueMax:
                        qValueMax=qValue
                        actionBestList=[]
                        actionBestList.append(actionTemp)
                        #actionBest=actionTemp
                    elif qValue==qValueMax:
                        actionBestList.append(actionTemp)
                if operatinType=='getMaxQ':
                    return qValueMax
                else:#getAction
                    global epsilon
                    global runCounter
                    if rd.random()<epsilon:
                    #    print '================random value: %f epsilon: %f ' % (rd.random(),epsilon)
                         actionBest=LearningAgent.randomSelectAnAction()
                    else: 
                      if len(actionBestList)>1:
                          actionBest=rd.choice(actionBestList)
                          return actionBest
                      else:
                          return actionBestList[0]
        elif operatinType=='getQ':#get q value for the given state and take the action
            if dictOfActionAndQs==defaultDict:#not exist
                return 0
            else:#for the given state, exist dict of actinAndQs==>if for the action exist value, return the value. else return 0.
                q=dictOfActionAndQs.get(action,0)
                return q
               
        
    def update(self, t):
        global qMatrixDict
        print  qMatrixDict
        global runCounter
        runCounter=runCounter+1
        global epsilon
        epsilon=epsilon*(0.95)
        #epsilon=self.get_decay_rate(runCounter)#runCounter
        global alpha
        alpha=alpha*(0.95) #self.get_decay_rate(runCounter)#runCounter
        #global GAMMA
        #GAMMA=self.get_decay_rate(runCounter)
        print runCounter
        #11111:Sense the agent state (here state s)--->  Gather inputs(state:s)
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        next_waypoint=self.next_waypoint
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
         
        # TODO: Update state
        self.state=".total reward"+str(totalReward)+" (total penalty:"+str(totalPenalty)+")",inputs,next_waypoint
        
        # TODO: Select action according to your policy
        action=self.getOrUpdateMaxQAction(inputs,next_waypoint,deadline,None,0,'getAction')
        print action
        global actionGG
        actionGG=action
        # 33333:Take the action and get the reward---->Execute action and get reward
        reward = self.env.act(self, action)
        global totalReward
        totalReward=totalReward+reward
        global totalPenalty
        if reward<0:
            totalPenalty=totalPenalty+reward
        # 4444:Sense the agent state (here state s')--->Gather inputs(state:s')
        next_waypoint2 = self.planner.next_waypoint()
        inputs2 = self.env.sense(self)
        deadline2 = deadline-1
       
        # TODO: Learn policy based on state, action, reward
        #5555 Calculate and update new Q value based on the formula
        maxQNextStateForAllPossibleAction=self.getOrUpdateMaxQAction(inputs2,next_waypoint2,deadline2,None,0,'getMaxQ') #get max q given the next state
        print action
        q=self.getOrUpdateMaxQAction(inputs,next_waypoint,deadline,action,0,'getQ') #get specific q value correspond to the action for the given state.
        global alpha
        global GAMMA
        #q=round(q+alpha*(reward+GAMMA*maxQNextStateForAllPossibleAction-q),7)
        #q=(1-alpha)*q+alpha*(reward+GAMMA*(maxQNextStateForAllPossibleAction-q))
        q=(1-alpha)*q+alpha*(reward+GAMMA*(maxQNextStateForAllPossibleAction))
        q=round(q,5)
        #q=round(q+alpha*(reward+GAMMA*maxQNextStateForAllPossibleAction-q),7)
        #update Q values Matrix
        self.getOrUpdateMaxQAction(inputs,next_waypoint,deadline,action,q,'updateQ')    
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]
    
def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track --->False

    # Now simulate it
    sim = Simulator(e, update_delay=0.001)  # reduce update_delay to speed up simulation 1.0
    sim.run(n_trials=10)  # press Esc or close pygame window to quit 10


if __name__ == '__main__':
    run()

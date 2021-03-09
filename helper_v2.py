import pandas as pd

def changeTargetNodeLabel(graph, targetNeoIdList):
#wrangle json so that target node is diff color
#replace label of entity with target
    for no, nodeDict in enumerate(graph['nodes']):
        if nodeDict['label'] == 'Entity':
            if nodeDict['NeoId'] in targetNeoIdList:
                graph['nodes'][no]['label'] = 'Target'

def getNetworkJson(df, graphDict, targetNeoIdCol = 'targetMuleAccountNeoIds'):
    #get 8 targets 
    allNeoIds = list(df['NeoIds'].values[0])
#     targetIds = df['targetMuleAccountID'].values[0]
    targetTransIds = df['TransIds'].values[0]
    targetNeoIds = df[targetNeoIdCol].values[0]

    #export target network to json
    jsonGraph = {}
    nodeInfo = [i for i in graphDict['nodes'] if i['NeoId'] in allNeoIds]
    linkInfo = [i for i in graphDict['links'] if i['transId'] in targetTransIds]
    #assumption: contact nodes are at receiving end
    contactNodes = [i['target'] for i in linkInfo if i['type'] == 'HAS_CONTACT']
    #all neo4j Id from unwanted contact nodes
    removeContactNodes = [i for i,j in dict(pd.Series(contactNodes).value_counts()).items() if j==1]

    #final linkInfo
    linkInfo2 = [i for i in linkInfo if i['target'] not in removeContactNodes]
    #final nodeINfo
    nodeInfo2 = [i for i in nodeInfo if i['NeoId'] not in removeContactNodes]
    
    #store node and links info
#     jsonGraph['nodes'] = nodeInfo
    jsonGraph['nodes'] = nodeInfo2
#     jsonGraph['links'] = linkInfo
    jsonGraph['links'] = linkInfo2
    
    #change label of target node
    changeTargetNodeLabel(jsonGraph, targetNeoIds)
    
    return jsonGraph

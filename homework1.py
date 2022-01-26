import pandas as pd
import math

data = pd.read_csv("id3_data.csv", delimiter=',')

# Auxiliary function to calculate the entropy given a target attribute
def entropy_calculator(data, target):
    n = sum(data[target].value_counts())
    target_entropy = sum([(i/n) * math.log(n/i, 2) for i in data[target].value_counts()])
    return target_entropy


# Auxiliary function to calculate the total tree entropy after each chosen attribute
def tree_entropy(data, target, branches):
    h = 0
    n = len(data)
    for i in branches:
        newdata = data
        for pair in branches[i]:
            newdata = newdata.loc[newdata[pair[0]] == pair[1]]
        h += (len(newdata)/n) * entropy_calculator(newdata, target)
    return h
    

# Main algorithm
def id3_algorithm(data):
    
    # First loop; deciding the root node of the tree
    attributes = list(data.keys()[:-1])
    target = data.keys()[-1]
    target_entropy = entropy_calculator(data, target)
    print(f'Initial entropy of the dataset = {target_entropy}\n')
    max_ig = 0
    for att in attributes:
        att_e = 0
        for val in data[att].unique():
            newdata = data.loc[data[att] == val]
            att_e += (len(newdata)/len(data)) * entropy_calculator(newdata, target)
        print(f'H( {target} | {att} ) = {att_e}')
        ig = target_entropy - att_e
        if ig > max_ig:
            max_ig = ig
            best_att = att    
    
    # Creating the structure
    known = [best_att]
    attributes.remove(best_att)
    branch_id = 1
    branches = {}
    for val in data[best_att].unique():
        branches[branch_id] = [(best_att, val)]
        branch_id += 1
    print(f'\nChosen attribute (node): {best_att}\nTotal tree entropy: {tree_entropy(data, target, branches)}\n')
    
    # Other loops; searching in which branch and for which attribute we get maximum IG
    paths = {}
    while attributes != []:
        max_ig = 0
        best_att = None
        best_branch = None
        for i in branches:
            to_remove = []
            newdata = data
            max_ig = 0
            aux = ''
            for pair in branches[i]:
                newdata = newdata.loc[newdata[pair[0]] == pair[1]]
                aux += str(pair[0])+' = '+str(pair[1])+', '
            target_entropy = entropy_calculator(newdata, target)
            if target_entropy != 0:
                for att in attributes:
                    att_e = 0
                    for val in newdata[att].unique():
                        newestdata = newdata.loc[newdata[att] == val]
                        att_e += (len(newestdata)/len(newdata)) * entropy_calculator(newestdata, target)
                    #aux = str()
                    print(f'H( {target} | {aux}{att} ) = {att_e}')
                    ig = target_entropy - att_e
                    if ig > max_ig:
                        max_ig = ig
                        best_att = att
                        best_branch = i
            else:
                print(f'H( {target} | {aux[:-2]} ) = 0')
                to_remove.append(i)
                if str(branches[i]) not in list(paths.keys()):
                    paths[str(branches[i])] = f'{target}= {newdata[target].unique()[0]}'
        
        for i in to_remove:
            branches.pop(i)

        if best_att:
            known.append(best_att)
            attributes.remove(best_att)
            path = branches[best_branch]
            branches.pop(best_branch)
            for val in data[best_att].unique():
                branches[branch_id] = path + [(best_att, val)]
                branch_id += 1
            print(f'\nChosen attribute: {best_att}\nTotal tree entropy: {tree_entropy(data, target, branches)}\n')
        else:
            break
            
    return paths


id3_algorithm(data)

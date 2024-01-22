import random
from copy import copy


def print_tree(tree, depth=0):
    """
    toon de boom maar gekanteld dus hij groeit van links naar rechts ipv van boven naar onder
    :param tree: de boom zelf
    :param depth: het niveau van de boom dat wordt afgedrukt (het indentatieniveau)
    :return: niets
    """
    keylist=[]
    if tree is None:
        print('%s' % ((depth * '\t') + str([])))
        return
    for e in tree.root:
        keylist.append(e.id)
    print('%s' % ((depth * '\t') + str(keylist)))
    ## als kinderen
    if len(tree.subTrees) != tree.subTrees.count(None):
        for subtree in tree.subTrees:
            print_tree(subtree, depth + 1)
class treeItem:
    def __init__(self,key,value=None):
        self.id=key
        self.value=value
class TwoThreeFourTree:
    def __init__(self):
        self.parentTree=None
        self.root=[]
        self.subTrees=[]
        self.N=3
    def inorderTraverse(self, function=print):
        """
        Loopt de zoeksleutels door van klein naar groot af
        en voert function uit op de obj value
        """
        if self.subTrees==[]:
            for obj in self.root:
                function(obj.value)
            return
        for i in range(0,len(self.subTrees)):
            if self.subTrees!=[]:
                self.subTrees[i].inorderTraverse(function)
            if i!=len(self.subTrees)-1:
                function(self.root[i].value)


    def retrieveItem(self,searchKey):
        """
        Geeft het treeItem zijn zoeksleutel terug met als zoeksleutel: searchKey
        :returns True if success else return False
        :returns treeItem
        """
        if self.root!=[]:
            for i in range(0,len(self.root)):
                if self.root[i].id==searchKey:
                    return (self.root[i].value,True)
                elif searchKey<self.root[i].id and self.subTrees!=[]:
                    returnvalue=self.subTrees[i].retrieveItem(searchKey)
                    return returnvalue
            if self.subTrees!=[]:
                returnvalue=self.subTrees[-1].retrieveItem(searchKey)
                return returnvalue
        return (None,False)
    def insertItem(self,newItem):
        """
        Deze method zal een item toevoegen aan de 2-3-4boom.
        input: item
        preconditie: De 2-3-4 boom bestaat.
        postconditie: Het item zal toegevoegd zijn aan de boom.
        :returns True if success else return False
        """
        if len(self.root)==self.N: #volle knoop
            currentTree=self.split()
            # currentTree.insertItem(newItem)
            for i in range(0,len(currentTree.root)):
                if newItem.id<currentTree.root[i].id:
                    currentTree.subTrees[i].insertItem(newItem)
                    return True
            currentTree.subTrees[len(currentTree.root)].insertItem(newItem)
            return True
        elif (len(self.root)<self.N) & (self.subTrees==[]): #insert in blad
            self.root.append(newItem)
            self.root.sort(key=lambda treeItem: treeItem.id)
        else:
            for i in range(0,len(self.root)):
                if newItem.id<self.root[i].id:
                    self.subTrees[i].insertItem(newItem)
                    return True
            if len(self.subTrees)==len(self.root):
                self.subTrees.append(TwoThreeFourTree())
                self.subTrees[len(self.root)].insertItem(newItem)
            else:
                self.subTrees[len(self.root)].insertItem(newItem)
            return True
        return True
    def deleteItem(self,searchKey):
        """
        Deze method zal het treeItem met zoeksleutel searchkey verwijderen uit de 2-3-4boom.
        input: item
        preconditie: De 2-3-4 boom bestaat.
        postconditie: het item zal verwijderd zijn uit de boom
        :returns True if success else return False

        """
        if self.isEmpty() and self.parentTree==None:
            return False
        if self.retrieveItem(searchKey)[1]==False:
            return False
        if self.parentTree != None and self.subTrees!=[] and len(self.root)==1: #2-knoop (geen root of blad)
            self.redistribute()
        if self.root!=[]:
            for i in range(0,len(self.root)):
                if searchKey==self.root[i].id:
                    if self.parentTree==None and self.subTrees==[]:
                        self.root.remove(self.root[i])
                        return True
                    elif self.subTrees==[] and len(self.root)>1: #blad
                        self.root.remove(self.root[i])
                        return True
                    elif self.subTrees==[] and len(self.root)==1: #blad
                        self.redistribute()
                        self.deleteItem(searchKey)
                        return True
                    elif self.subTrees!=[]:
                        successor=self.subTrees[i+1].inorderSuccessor(self.root[i],searchKey)
                        if successor==None:
                            self.deleteItem(searchKey)
                            return True
                        else:
                            self.swap(searchKey,successor) #rechterkind
                            return True
                elif searchKey<self.root[i].id and self.subTrees!=[]:
                    returnvalue= self.subTrees[i].deleteItem(searchKey)
                    return returnvalue
            if self.subTrees!=[]: #als het in de meest rechtse subTree zit
                returnvalue=self.subTrees[len(self.root)].deleteItem(searchKey)
        else:
            returnvalue=self.parentTree.deleteItem(searchKey)

        return returnvalue

    def redistribute(self):
        """
        Deze methode mag enkel opgeroepen worden door deleteItem en inorderSuccessor

        """
        if self.parentTree.subTrees.index(self) >= 1 and self.parentTree.subTrees.index(self) < len(self.parentTree.subTrees) - 1:  # middenkinderen
            if len(self.parentTree.subTrees[self.parentTree.subTrees.index(self) - 1].root) > 1:  # linkersibling
                self.redistributeL()
            elif len(self.parentTree.subTrees[self.parentTree.subTrees.index(self) + 1].root) > 1:  # rechtersibling
                self.redistributeR()
            else:
                self.mergeL()
        elif self.parentTree.subTrees.index(self) == 0:  # meest linkse kind
            if len(self.parentTree.subTrees[1].root) > 1:  # rechtersibling
                self.redistributeR()
            else:
                self.mergeR()
        elif self.parentTree.subTrees.index(self) == len(self.parentTree.subTrees) - 1:  # meest rechtse kind
            if len(self.parentTree.subTrees[self.parentTree.subTrees.index(self) - 1].root) > 1:
                self.redistributeL()
            else:
                self.mergeL()

    def redistributeL(self):
        """
            Deze methode mag enkel opgeroepen worden door deleteItem en redistribute

        """
        self.root.append(self.parentTree.root.pop(self.parentTree.subTrees.index(self) - 1))
        self.parentTree.root.append(self.parentTree.subTrees[self.parentTree.subTrees.index(self) - 1].root.pop(-1))
        self.parentTree.root.sort(key=lambda treeItem: treeItem.id)
        self.root.sort(key=lambda treeItem: treeItem.id) #insert(0) instead
        if self.parentTree.subTrees[self.parentTree.subTrees.index(self)-1].subTrees!=[]:
            self.subTrees.insert(0,self.parentTree.subTrees[self.parentTree.subTrees.index(self)-1].subTrees.pop(-1))
            self.subTrees[0].parentTree=self

    def redistributeR(self):
        """
            Deze methode mag enkel opgeroepen worden door deleteItem en redistribute

        """
        self.root.append(self.parentTree.root.pop(self.parentTree.subTrees.index(self)))
        self.parentTree.root.append(self.parentTree.subTrees[self.parentTree.subTrees.index(self) + 1].root.pop(0))
        self.parentTree.root.sort(key=lambda treeItem: treeItem.id)
        self.root.sort(key=lambda treeItem: treeItem.id)
        if self.parentTree.subTrees[self.parentTree.subTrees.index(self)+1].subTrees!=[]:
            self.subTrees.append(self.parentTree.subTrees[self.parentTree.subTrees.index(self)+1].subTrees.pop(0))
            self.subTrees[-1].parentTree=self

    def mergeL(self):
        """
            Deze methode mag enkel opgeroepen worden door deleteItem en redistribute

        """
        if self.parentTree.parentTree==None and len(self.parentTree.root)==1:
            self.parentTree.mergeRoot()
            return

        #eerst parent, dan sibling
        self.root.insert(0,self.parentTree.root.pop(self.parentTree.subTrees.index(self) - 1))
        if self.parentTree.subTrees[self.parentTree.subTrees.index(self) - 1].subTrees!=[]:
            self.subTrees.insert(0,self.parentTree.subTrees[self.parentTree.subTrees.index(self) - 1].subTrees.pop(-1))
            self.subTrees[0].parentTree = self
            self.subTrees.insert(0,self.parentTree.subTrees[self.parentTree.subTrees.index(self) - 1].subTrees.pop(-1))
            self.subTrees[0].parentTree = self
        self.root.insert(0,self.parentTree.subTrees[self.parentTree.subTrees.index(self) - 1].root.pop(-1))
        del self.parentTree.subTrees[self.parentTree.subTrees.index(self)-1]

    def mergeR(self):
        """
            Deze methode mag enkel opgeroepen worden door deleteItem en redistribute

        """
        if self.parentTree.parentTree==None and len(self.parentTree.root)==1:
            self.parentTree.mergeRoot()
            return

        # eerst parent append, dan sibling
        self.root.append(self.parentTree.root.pop(0))
        if self.parentTree.subTrees[1].subTrees!=[]:
            self.subTrees.append(self.parentTree.subTrees[1].subTrees.pop(0))
            self.subTrees[-1].parentTree=self
            self.subTrees.append(self.parentTree.subTrees[1].subTrees.pop(0))
            self.subTrees[-1].parentTree = self
        self.root.append(self.parentTree.subTrees[1].root.pop(0))
        del self.parentTree.subTrees[1]
        # if self.parentTree.parentTree==None and self.parentTree.root==[]:
        #     self.parentTree.root=self.root
        #     self.parentTree.subTrees=self.subTrees

    def mergeRoot(self):
        """
            Deze methode mag enkel opgeroepen worden door deleteItem en redistribute

        """
        self.root.insert(0,self.subTrees[0].root[0])
        self.root.append(self.subTrees[1].root[0])
        if self.subTrees[0].subTrees!=[]: #gebalanceerde boom dus geldt ook voor subtrees[1] (als alles toch werkt)
            self.subTrees.append(self.subTrees[0].subTrees.pop(0))
            self.subTrees.append(self.subTrees[0].subTrees.pop(0))
            self.subTrees.append(self.subTrees[1].subTrees.pop(0))
            self.subTrees.append(self.subTrees[1].subTrees.pop(0))
            self.subTrees[0].root.clear()
            self.subTrees[1].root.clear()
            self.subTrees.pop(0)
            self.subTrees.pop(0)
            self.subTrees[0].parentTree = self
            self.subTrees[1].parentTree = self
            self.subTrees[2].parentTree = self
            self.subTrees[3].parentTree = self
        else:
            self.subTrees[0].root.clear()
            self.subTrees[1].root.clear()
            self.subTrees.pop(0)
            self.subTrees.pop(0)
            
    def inorderSuccessor(self, item, searchKey):
        """
            Deze methode mag enkel opgeroepen worden door deleteItem

        """
        if len(self.root)==1:
            self.redistribute()
        if self.subTrees!=[]:
            for i in range(0,len(self.root)):
                if searchKey<self.root[i].id:
                    return self.subTrees[i].inorderSuccessor(item, searchKey)
        elif self.subTrees==[]:
            if self.root!=[] and (item not in self.root) :
                return self.root.pop(0)
            else:
                return None

    def swap(self,searchKey,successor):
        """
        Deze methode mag enkel opgeroepen worden door deleteItem

         """
        for i in range(0,len(self.root)):
            if self.root[i].id==searchKey:
                self.root[i]=successor
                return
            elif searchKey<self.root[i].id:
                self.subTrees[i].swap(searchKey,successor)
                return
        self.subTrees[-1].swap(searchKey,successor)
        return

    def split(self):
        """
        Deze methode mag enkel opgeroepen worden door insertItem

        """
        if self.parentTree==None:
            newTree1=TwoThreeFourTree()
            newTree2=TwoThreeFourTree()
            newTree1.parentTree=self
            newTree2.parentTree=self
            newTree1.root.append(self.root.pop(0))
            newTree2.root.append(self.root.pop(1))
            if self.subTrees!=[]:
                self.subTrees[0].parentTree = newTree1
                self.subTrees[1].parentTree = newTree1
                newTree1.subTrees.append(self.subTrees.pop(0))
                newTree1.subTrees.append(self.subTrees.pop(0))
                self.subTrees[0].parentTree = newTree2
                self.subTrees[1].parentTree = newTree2
                newTree2.subTrees.append(self.subTrees.pop(0))
                newTree2.subTrees.append(self.subTrees.pop(0))
            self.subTrees.append(newTree1)
            self.subTrees.append(newTree2)
            return self
        else:
            self.parentTree.root.append(self.root.pop(1))
            self.parentTree.root.sort(key=lambda treeItem: treeItem.id)
            newTree=TwoThreeFourTree()
            newTree.parentTree=self.parentTree
            self.parentTree.subTrees.insert(self.parentTree.subTrees.index(self)+1,newTree)
            # self.parentTree.subTrees.append(newTree)
            newTree.root.append(self.root.pop(1))
            if len(self.subTrees)==2:
                self.subTrees[1].parentTree = newTree
                newTree.subTrees.append(self.subTrees.pop(1))
            elif len(self.subTrees)==4:
                self.subTrees[2].parentTree = newTree
                self.subTrees[3].parentTree = newTree
                newTree.subTrees.append(self.subTrees.pop(2))
                newTree.subTrees.append(self.subTrees.pop(2))
            return self.parentTree

    def save(self):
        """
        Deze method zal de 2-3-4 boom opslagen als dict
        preconditie: De boom bestaat
        postconditie: De boom blijft ongewijzigd en er zal een dict zijn gemaakt
        die de boom voorsteld.
        """
        boom = dict()
        l=list()
        for treeitem in self.root:
            l.append(treeitem.id)
        boom["root"]=l
        q=list()
        if self.subTrees!=[]:
            for tree in self.subTrees:
                q.append(tree.save())
        else:
            return boom
        boom["children"]=q
        return boom

    def load(self,dictionary):
        """
        Deze method zal de 2-3-4 boom opstellen aan de hand van de gegeven dictionary
        preconditie: De boom bestaat
        postconditie: De boom blijft ongewijzigd en er zal een dict zijn gemaakt
        die de boom voorsteld.
        """
        self.root=[]
        self.subTrees=[]
        l=list()
        if "root" in dictionary:
            for key in dictionary["root"]:
                l.append(treeItem(key))
            self.root=l
        if "children" in dictionary:
            i=0
            for dic in dictionary["children"]:
                self.subTrees.append(TwoThreeFourTree())
                self.subTrees[-1].parentTree=self
                self.subTrees[i].load(dic)
                i+=1
        return
    def isEmpty(self):
        if self.root==[]:
            return True
        else:
            return False

boom=TwoThreeFourTree()
# boom.insertItem(treeItem(10,"tien"))
# boom.insertItem(treeItem(5,"vijf"))
# boom.insertItem(treeItem(15,"vijftien"))
# boom.insertItem(treeItem(20,"twintig"))
# boom.insertItem(treeItem(25,"vijfentwintig"))
# boom.insertItem(treeItem(30,"vijfentwintig"))
# boom.insertItem(treeItem(35,"vijfentwintig"))
# boom.insertItem(treeItem(40,"vijfentwintig"))
# boom.insertItem(treeItem(45,"vijfentwintig"))
# for i in range(0,100):
#     boom.insertItem(treeItem(random.randint(0,100),"timisnigay"))
# boom.inorder()
# print_tree(boom)
# print(boom.deleteItem(10))
# print(boom.deleteItem(20))
# print(boom.retrieveItem(46))
# print_tree(boom)


# boom.insertItem(treeItem(70,"vijfentwintig"))
# boom.insertItem(treeItem(70,"vijfen"))
# boom.insertItem(treeItem(70,"vijfentig"))
# boom.insertItem(treeItem(70,"vijfentig"))
# print(boom.retrieveItem(65))
boom.insertItem(treeItem(55,"vijfentwintig"))
boom.insertItem(treeItem(80,"vijfentwintig"))
boom.insertItem(treeItem(90,"vijfentwintig"))
boom.insertItem(treeItem(85,"vijfentwintig"))
boom.insertItem(treeItem(95,"vijfentwintig"))
boom.insertItem(treeItem(100,"vijfentwintig"))
boom.insertItem(treeItem(105,"vijfentwintig"))
boom.insertItem(treeItem(110,"vijfentwintig"))
boom.insertItem(treeItem(115,"vijfentwintig"))
boom.insertItem(treeItem(120,"vijfentwintig"))
boom.insertItem(treeItem(125,"vijfentwintig"))
boom.insertItem(treeItem(130,"vijfentwintig"))
boom.deleteItem(122)
boom.deleteItem(120)
boom.insertItem(treeItem(121, "vijfen"))
boom.deleteItem(122)
boom.deleteItem(125)
boom.deleteItem(122)

boom.deleteItem(121)
print_tree(boom)

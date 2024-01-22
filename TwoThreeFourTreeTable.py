from TwoThreeFourTree import TwoThreeFourTree
class TwoThreeFourTreeTable:
    def __init__(self):
        self.tree=TwoThreeFourTree()

    def tableInsert(self,newItem):
        return self.tree.insertItem(newItem)

    def tableIsEmpty(self):
        return self.tree.isEmpty()

    def tableDelete(self, searchKey):
        return self.tree.deleteItem(searchKey)

    def tableRetrieve(self, searchKey):
        return self.tree.retrieveItem(searchKey)

    def traverseTable(self,function):
        return self.tree.inorderTraverse(function)

    def save(self):
        return self.tree.save()

    def load(self, dictionary):
        return self.tree.load(dictionary)
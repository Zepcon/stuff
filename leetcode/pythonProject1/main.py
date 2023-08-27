# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
         self.val = val
         self.next = next

    def __str__(self):
        return "val:"+str(self.val) +" next:"+ str(self.next)


class Solution:
    def addTwoNumbers(self, l1: [ListNode], l2: [ListNode]) -> [ListNode]:
        temp1, temp2 = [],[]
        # temp1
        for i in l1[:-1]:
            temp1.append(i.val)
        if len(l1) > 1:
            temp1.append(l1[-1].val)
            if l1[-1].next is not None:
                temp1.append(l1[-1].next)
        # temp2
        for i in l2[:-1]:
            temp2.append(i.val)
        if len(l2) > 1:
            temp1.append(l2[-1].val)
            if l2[-1].next is not None:
                temp2.append(l2[-1].next)

        temp1.reverse()
        temp2.reverse()

        t1num = int(''.join([str(n) for n in temp1]))
        t2num = int(''.join([str(n) for n in temp2]))

        sum = t1num + t2num

        sum = list(map(int,str(sum)))
        sum.reverse()

        ret = []
        for i in range(0,len(sum),2):
            ret.append(ListNode(sum[i],sum[i+1]))

        if len(sum) % 2 != 0:
            ret.append(ListNode(sum[-1]))

        for i in ret:
            print(i)
        return ret

l1 = [ListNode(2,4),ListNode(4,3)]
l2 = [ListNode(5,6),ListNode(6,4)]

er = Solution()
er.addTwoNumbers(l1,l2)

print()
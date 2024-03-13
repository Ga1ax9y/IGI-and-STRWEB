
def Min_modul(arr):
    print("Номер минимального по модулю:",arr.index((min(arr,key=abs)))+1)

def Sum_after(arr):
    result = 0
    first = 0
    for i in range(len(arr)):
        if arr[i]>0:
            first = i+1
            break
    for num in arr[first:]:
        result+=num
    print(result)



def list_work():
    arr = []
    n = int(input())
    for i in range(n):
        d = float(input())
        arr.append(d)
    Min_modul(arr)
    Sum_after(arr)
list_work()

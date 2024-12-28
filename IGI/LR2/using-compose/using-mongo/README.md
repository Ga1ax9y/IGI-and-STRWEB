## Using Nodejs + MongoDB 


```
 docker compose up -d --build
```



<img width="712" alt="image" src="https://github.com/ajeetraina/todo-list/assets/313480/895966f9-4e3d-46d6-a9b3-964c45d65ba4">


<img width="1143" alt="image" src="https://github.com/ajeetraina/todo-list/assets/313480/f93d4da7-ecfb-4242-910f-265957d98225">


## Interacting with Mongo using Docker Dashboard Container Console


<img width="1172" alt="image" src="https://github.com/ajeetraina/todo-list/assets/313480/8e4486c5-807d-46a1-9159-500c7ef20c0b">


## Populating todo-List Items

<img width="681" alt="image" src="https://github.com/ajeetraina/todo-list/assets/313480/58050bdd-d5f2-47d4-99b4-c976620844e9">



```
test> show dbs
admin       40.00 KiB
config      12.00 KiB
local       40.00 KiB
node-mongo  40.00 KiB
test> use node-mongo
switched to db node-mongo
node-mongo> show collections
items
node-mongo>
```

```
db.items.find()
[
  {
    _id: ObjectId('65b8b820e9f51f3c974aa700'),
    title: 'Watch Netflix',
    description: 'Renew the netflix account',
    date: ISODate('2024-01-30T08:49:36.151Z'),
    __v: 0
  },
  {
    _id: ObjectId('65b8b84be9f51f3c974aa703'),
    title: 'Buy Grocery',
    description: 'Carry purse and buy grocery',
    date: ISODate('2024-01-30T08:50:19.520Z'),
    __v: 0
  }
]
```



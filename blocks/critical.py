def Value(criticality):
    return {            
        "critical-time" : criticality
        }
        
High = Value( range(1,5))

Medium = Value( range(5,10))

Low = Value( range(10,15))


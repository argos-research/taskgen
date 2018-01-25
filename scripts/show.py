#!/usr/local/bin/python3
import numpy as np
import matplotlib.pyplot as plt


t_data = np.genfromtxt('tasks_1m.csv', delimiter=',', skip_header=10,
                     skip_footer=10, names=['tasks', 'variants', 'memory', 'xml', 'generator', 'description'])

v_data = np.genfromtxt('variants_1m.csv', delimiter=',', skip_header=10,
                     skip_footer=10, names=['tasks', 'variants', 'memory', 'xml', 'generator', 'description'])


# tasks vs {generator, description}
plt.subplot(2,2,1)
plt.plot(t_data['tasks'], t_data['generator'], color='r', label='Variant Calculation')
plt.plot(t_data['tasks'], t_data['description'], color='b', label='Description Calculation')
plt.xlabel('Tasks')
plt.ylabel('Time (microseconds)')
plt.legend()

# variants vs {generator, description}
plt.subplot(2,2,2)
plt.plot(v_data['variants'], v_data['generator'], color='r', label='Variant Calculation')
plt.plot(v_data['variants'], v_data['description'], color='b', label='Description Calculation')
plt.xlabel('Varianten')
plt.ylabel('Time (microseconds)')
plt.legend()

# {tasks, variants} vs memory
plt.subplot(2,2,3)
plt.plot(t_data['tasks'], t_data['memory'], color='yellow', label='Number of Tasks')
plt.plot(v_data['variants'], v_data['memory'], color='green', label='Number of Variants')
plt.xlabel('Tasks/Variants')
plt.ylabel('Memory')
plt.xlim(0,100000)
plt.legend()

# {tasks, variants} vs xml
plt.subplot(2,2,4)
plt.plot(t_data['tasks'], t_data['xml'], color='yellow', label='Number of Tasks')
plt.plot(v_data['variants'], v_data['xml'], color='green', label='Number of Variants')
plt.xlabel('Tasks/Variants')
plt.xlim(0,100000)
plt.ylabel('XML')
plt.legend()



plt.show()

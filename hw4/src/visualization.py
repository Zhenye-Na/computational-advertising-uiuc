"""
HW4: Ads analysis.

Visualization.

@author: Zhenye Na
"""

import numpy as np
import matplotlib.pyplot as plt

ontology = ["gender", "ethnicity", "location", "career", "age",
            "marriage", "education", "price", "season", "social"]

count = [5,
         2,
         1,
         23,
         3,
         0,
         17,
         1,
         0,
         4]

y_pos = np.arange(len(ontology))

plt.barh(y_pos, count, align='center', alpha=0.5)
plt.yticks(y_pos, ontology)
plt.xlabel('Count')
plt.title('Advertisement Analysis')


plt.show()
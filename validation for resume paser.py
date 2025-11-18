from sentence_transformers import SentenceTransformer, util
from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np
import random

# Load model
model = SentenceTransformer('all-MiniLM-L5-v2')

# Simulate 1000 resumes 
skills_pool = [
    "Python", "JavaScript", "React", "Node.js", "SQL", "AWS", "Machine Learning",
    "Data Analysis", "Arabic", "Java", "Django", "Flask", "Docker", "Kubernetes",
    "TensorFlow", "Pandas", "Excel", "Communication", "Leadership", "Time Management"
]

resumes = []
for _ in range(1000):
    chosen_skills = random.sample(skills_pool, random.randint(4, 8))
    resumes.append(" ".join(chosen_skills))

# job queries
queries = [
    "Python developer with Flask and Docker experience",
    "Data analyst proficient in SQL and Excel",
    "Machine Learning engineer with TensorFlow knowledge",
    "Web developer using JavaScript and React",
    "AWS certified cloud engineer",
    "Backend developer with Node.js and MongoDB",
    "Fluent in Arabic with data visualization skills",
    "Strong communicator with leadership qualities",
    "Java developer with Spring Boot",
    "Time management and communication expert"
]

# Simulated correct matches 
ground_truth = [set(range(10)) for _ in queries]

# Encode
resume_embeddings = model.encode(resumes, convert_to_tensor=True)
query_embeddings = model.encode(queries, convert_to_tensor=True)

# Validate
top_n = 10
precision_list, recall_list, f1_list = [], [], []

for idx, q_embed in enumerate(query_embeddings):
    cos_scores = util.pytorch_cos_sim(q_embed, resume_embeddings)[0]
    top_indices = np.argpartition(-cos_scores, range(top_n))[:top_n]

    y_true = [1 if i in ground_truth[idx] else 0 for i in range(1000)]
    y_pred = [1 if i in top_indices else 0 for i in range(1000)]

    precision_list.append(precision_score(y_true, y_pred))
    recall_list.append(recall_score(y_true, y_pred))
    f1_list.append(f1_score(y_true, y_pred))

# Final metrics
print("Precision:", round(np.mean(precision_list)*100, 2), "%")
print("Recall:", round(np.mean(recall_list)*100, 2), "%")
print("F1-Score:", round(np.mean(f1_list)*100, 2), "%")

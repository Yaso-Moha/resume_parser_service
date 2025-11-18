from sklearn.metrics import classification_report, precision_score, recall_score, f1_score


# y_true: actual human labels
# y_pred: predicted labels from the MiniLM scoring pipeline

y_true = ['Excellent', 'Good', 'Fair', 'Excellent', 'Poor', 'Good', 'Fair', 'Excellent']
y_pred = ['Excellent', 'Fair', 'Fair', 'Good', 'Poor', 'Good', 'Fair', 'Excellent']

# Generate a full classification report
print(classification_report(y_true, y_pred, digits=2))

# Compute individual metrics if needed
precision = precision_score(y_true, y_pred, average='macro')  # macro = treats all classes equally
recall = recall_score(y_true, y_pred, average='macro')
f1 = f1_score(y_true, y_pred, average='macro')

print("Precision:", round(precision * 100, 2), "%")
print("Recall:", round(recall * 100, 2), "%")
print("F1 Score:", round(f1 * 100, 2), "%")

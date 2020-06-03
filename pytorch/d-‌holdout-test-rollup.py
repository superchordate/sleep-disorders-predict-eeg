from sklearn.metrics import classification_report

# Check validation set after each epoch.
for local_batch, local_labels, file in holdout:
    
    if torch.cuda.is_available():
        local_batch = local_batch.cuda()
        local_labels = local_labels.cuda()
    
    local_labels = local_labels.view(local_labels.size(0), 1)
    outputs = net(local_batch)
    predictions = np.array([int(i) for i in outputs.max(dim = 1)[1]])
    labels =  np.array([int(i) for i in local_labels])
    
results = pd.DataFrame({
    'file': file,
    'label': labels, 
    'prediction': predictions
})
results['file'] = results.file.str.extract(r'holdout/([^-]+)-')
sm = results.groupby('file')['prediction'].agg('mean').reset_index()
sm['prediction'] = (sm.prediction > .5) * 1
sm['label'] = sm.file.str.contains(disorder) * 1

print(
  classification_report(sm.label, sm.prediction)
 )
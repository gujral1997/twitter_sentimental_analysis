import tweetment
import datetime
import csv
classifier = tweetment.SentimentClassifier('./model.pkl')
print "Model Has Started"
i =1
positive=0
negative=0
neutral=0
tweets=[]
sentiments=[]
with open('politics.csv', 'rb') as f:
    mycsv = csv.reader(f)
    for row in mycsv:
        row = ''.join(map(str, row))
        tweets.append(row)
        try:
            sentiment = classifier.classify(row)
            if (sentiment =='positive'):
                positive+=1
            elif (sentiment =='negative'):
                negative+=1
            elif (sentiment =='neutral'):
                neutral+=1
        except:
            pass
        sentiments.append(sentiment)

print "writing predictions now"

with open('non_tech_pred.csv', 'a') as csvfile:
    fieldnames = ['tweets', 'sentiment']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    #writer.writeheader()
    try:
        while (sentiments[i]):
            writer.writerow({'tweets': tweets[i], 'sentiment': sentiments[i]})
            i+=1
    except:
        pass

print "Positive tweets are: ", positive
print "Negative tweets are: ", negative
print "Neutral tweets are: ", neutral
print "Total tweets are: ", positive+negative+neutral

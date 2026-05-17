from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix


emails = [

    "Verify your bank account immediately",
    "Click here to win free money",
    "Your PayPal account is suspended",
    "Urgent login required now",
    "Claim your lottery prize today",
    "Update your password immediately",
    "You won a free iPhone",
    "Bank account verification needed",
    "Click this suspicious link now",
    "Limited offer claim reward",

    "Project meeting scheduled tomorrow",
    "Please submit assignment before Friday",
    "Lunch at 1 PM today",
    "Your order has been delivered",
    "Happy birthday have a great day",
    "Team meeting postponed",
    "Invoice attached for your purchase",
    "Can we arrange a call tomorrow",
    "Thank you for your support",
    "Your interview is scheduled"
]


labels = [
    1,1,1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0,0,0
]


vectorizer = CountVectorizer()

X = vectorizer.fit_transform(emails)

y = labels


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42
)


model = MultinomialNB()

model.fit(X_train, y_train)


predictions = model.predict(X_test)


accuracy = accuracy_score(y_test, predictions)

print("===================================")
print(" MACHINE LEARNING PHISHING DETECTOR")
print("===================================")

print("\nAccuracy:", round(accuracy * 100, 2), "%")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions))


while True:

    print("\n===================================")

    user_email = input(
        "Enter Email Text (type 'exit' to stop): "
    )

    if user_email.lower() == "exit":
        break

    email_vector = vectorizer.transform([user_email])

    result = model.predict(email_vector)

    if result[0] == 1:
        print("\n⚠ PHISHING EMAIL DETECTED")
    else:
        print("\n✅ SAFE EMAIL")
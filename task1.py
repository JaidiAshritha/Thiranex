import re

common_passwords = ["123456", "password", "qwerty", "admin"]

def check_strength(password):
    score = 0
    feedback = []
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers")

    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Add special characters")

    if password.lower() in common_passwords:
        return "Very Weak", ["This is a common password"]

    
    if score <= 2:
        return "Weak", feedback
    elif score <= 4:
        return "Medium", feedback
    else:
        return "Strong", feedback



pwd = input("Enter password: ")
strength, tips = check_strength(pwd)

print("Strength:", strength)
for tip in tips:
    print("-", tip)
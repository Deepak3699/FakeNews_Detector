from model import predict_news

# Test with sample texts
fake_text = """
BREAKING: Scientists SHOCKED by this ONE weird trick! 
Doctors HATE him! Click NOW before government BANS this!!!
"""



real_text = """
The Federal Reserve announced today that interest rates will remain 
unchanged following their monthly policy meeting. Economic analysts 
suggest this decision reflects ongoing concerns about inflation.
"""

print("=" * 60)
print("Testing FAKE news detection:")
print("=" * 60)
result = predict_news(fake_text)
print(result)

print("\n" + "=" * 60)
print("Testing REAL news detection:")
print("=" * 60)
result = predict_news(real_text)
print(result)
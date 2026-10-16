import boto3

client = boto3.client("bedrock-runtime", region_name="eu-north-1")

response = client.converse(
    modelId="eu.amazon.nova-micro-v1:0", messages=[{
    "role": "user",
    "content": [
        {
            "text": "Hello this is my first time using Bedrock, can you tell me an classic joke?"
        }
    ]
}]
    )

print(response["output"]["message"]["content"][0]["text"])
print(response["usage"])
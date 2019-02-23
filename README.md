# bin/ 下にheadless-chromium を追加する
 mkdir -p bin/
 curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
 unzip headless-chromium.zip -d bin/
 rm headless-chromium.zip

# chromedriverをダウンロード bin/ 下に
 curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip
 unzip chromedriver.zip -d bin/
 rm chromedriver.zip

# docker-image を作成
 - docker build -t lambda_headless_chrome .
 - docker run -v "${PWD}":/var/task lambda_headless_chrome

# labda関数に
- aws s3 cp deploy_package.zip s3://YOUR_BUCKET_NAME
- aws lambda create-function --region ap-northeast-1 --function-name lambda_headless_chrome_python --runtime -        - python3.6 --role YOUR_ROLE_NAME --code S3Bucket=YOUR_BUCKET_NAME,S3Key=deploy_package.zip --handler - - -          
- lambda_function.lambda_handler --memory-size 512 --timeout 300

#参考にしたサイト
https://qiita.com/nabehide/items/754eb7b7e9fff9a1047d
https://pvnotora.com/python-scraping-docker-for-lambda/
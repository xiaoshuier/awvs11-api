const https = require('https');

const options = {
  hostname: 'www.baidu.com',
  port: 443,
  path: '/s?wd=%E9%A3%9E%E4%B9%A6%E5%AE%98%E7%BD%91%E4%B8%8B%E8%BD%BD',
  method: 'GET',
  headers: {
    'User-Agent': 'Mozilla/5.0 (Node.js)'
  }
};

const req = https.request(options, (res) => {
  let data = '';

  // 接收数据
  res.on('data', (chunk) => {
    data += chunk;
  });

  // 数据接收完成
  res.on('end', () => {
    console.log('🔍 百度首页 HTML 内容（前500字预览）:\n');
    console.log(data); // 只打印前 500 字
  });
});

req.on('error', (e) => {
  console.error(`请求出错: ${e.message}`);
});

req.end();

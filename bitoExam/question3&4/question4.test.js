const axios = require('axios');

describe('trading-history pair', () => {

  it('200 usdt_twd resolution 1m', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/usdt_twd', { params: { resolution: '1m', from: 1550822974, to: 1566375034} });
    // console.log(response)
    // 斷言回應的狀態碼為 200
    expect(response.status).toBe(200);
    // console.log(response.data)
  })

  it('200 usdt_twd resolution 5m : response require key', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/usdt_twd', { params: { resolution: '5m', from: 1550822974, to: 1566375034} });
    // console.log(response)
    // 斷言回應的狀態碼為 200
    expect(response.status).toBe(200);
    expect(response.data.data[0]).toHaveProperty('timestamp')
    expect(response.data.data[0]).toHaveProperty('open')
    expect(response.data.data[0]).toHaveProperty('high')
    expect(response.data.data[0]).toHaveProperty('low')
    expect(response.data.data[0]).toHaveProperty('close')
    expect(response.data.data[0]).toHaveProperty('volume')
  })



  it('200 matic_usdt resolution 6h', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/matic_usdt', { params: { resolution: '6h', from: 1550822974, to: 1566375034} });
    // console.log(response)
    // 斷言回應的狀態碼為 200
    expect(response.status).toBe(200);

  })

  it('200 bito_twd resolution 1d : check data type is legal', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/bito_twd', { params: { resolution: '1d', from: 1550822974, to: 1566375034} });
    // console.log(response)
    // 斷言回應的狀態碼為 200
    expect(response.status).toBe(200);
    console.log(response.data.data[0])
    expect(typeof response.data.data[0]['timestamp']).toBe("string")
    expect(typeof response.data.data[0]['open']).toBe("string")
    expect(typeof response.data.data[0]['high']).toBe("string")
    expect(typeof response.data.data[0]['low']).toBe("string")
    expect(typeof response.data.data[0]['close']).toBe("string")
    expect(typeof response.data.data[0]['volume']).toBe("string")

  })

  it('200 btc_twd check timestamp between from and to', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/btc_twd', { params: { resolution: '3h', from: 1550822974, to: 1566375034} });
    // console.log(response)
    // 斷言回應的狀態碼為 200
    expect(response.status).toBe(200);
    // console.log(response.data)
    data = response.data.data
    data.forEach(function(item, i){
      console.log(i, item)
      expect(item['timestamp'] / 1000).toBeLessThanOrEqual(1566375034)
      expect(item['timestamp'] / 1000).toBeGreaterThanOrEqual(1550822974)
    });
  })


  it('200 btc_twd check timestamp gap same as resolution', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/btc_twd', { params: { resolution: '1h', from: 1550822974, to: 1566375034} });
    // console.log(response)
    // 斷言回應的狀態碼為 200
    expect(response.status).toBe(200);
    // console.log(response.data)
    data = response.data.data
    data.forEach(function(item, i){
      if(i != 0){
        expect(item['timestamp'] - data[i - 1]['timestamp']).toBe(3600000)
      }
    });
  })

  it('200 ape_twd ', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/ape_twd', { params: { resolution: '3h', from: 1550822974, to: 1566375034} });
    // console.log(response)
    // 斷言回應的狀態碼為 200
    expect(response.status).toBe(200);

    // console.log(response.data)
  })

  it('200 mv_twd', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/mv_twd', { params: { resolution: '3h', from: 1550822974, to: 1566375034} });
    // console.log(response)
    // 斷言回應的狀態碼為 200
    expect(response.status).toBe(200);
    // console.log(response.data)

  })

  it('200 gadt_twd', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/gadt_twd', { params: { resolution: '3h', from: 1550822974, to: 1566375034} });
    // console.log(response)
    // 斷言回應的狀態碼為 200
    expect(response.status).toBe(200);
    // console.log(response.data)

  })

  it('200 eos_twd', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/eos_twd', { params: { resolution: '3h', from: 1550822974, to: 1566375034} });
    // console.log(response)
    // 斷言回應的狀態碼為 200
    expect(response.status).toBe(200);
    // console.log(response.data)

  })


  it('200 ton_twd', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/ton_twd', { params: { resolution: '3h', from: 1550822974, to: 1566375034} });
    // console.log(response)
    // 斷言回應的狀態碼為 200
    expect(response.status).toBe(200);
    // console.log(response.data)

  })

  it('200 xrp_twd', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/xrp_twd', { params: { resolution: '3h', from: 1550822974, to: 1566375034} });
    // console.log(response)
    // 斷言回應的狀態碼為 200
    expect(response.status).toBe(200);
    // console.log(response.data)

  })


  it('200 matic_usdt', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/matic_usdt', { params: { resolution: '3h', from: 1550822974, to: 1566375034} });
    // console.log(response)
    // 斷言回應的狀態碼為 200
    expect(response.status).toBe(200);
    // console.log(response.data)

  })
  it('200 yfi_usdt', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/yfi_usdt', { params: { resolution: '3h', from: 1550822974, to: 1566375034} });
    // console.log(response)
    // 斷言回應的狀態碼為 200
    expect(response.status).toBe(200);
    // console.log(response.data)

  })



  it('422 error resolution 2h', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/ape_twd', { params: { resolution: '2h', from: 1550822974, to: 1566375034} , validateStatus: (status) => status === 422 });
    // console.log(response.status)
    // console.log('---------------')
    expect(response.status).toBe(422);
    expect(response.data.error).toBe('Resolution error');
  })

  it('422 error from', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/ape_twd', { params: { resolution: '3h', from: 15508229741, to: 1566375034} , validateStatus: (status) => status === 422 });
    // console.log(response.status)
    // console.log('---------------')
    expect(response.status).toBe(422);
    expect(response.data.error).toBe("Wrong parameter: Parameter `From` need to be less or equal to `To`");
  })

  it('422 error to', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/ape_twd', { params: { resolution: '3h', from: 15508229741, to: 156637503411} , validateStatus: (status) => status === 422 });
    // console.log(response.status)
    // console.log('---------------')
    expect(response.status).toBe(422);
    expect(response.data.error).toBe("Wrong parameter: timestamp out of range");
  })

  it('422 lack of resolution', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/ape_twd', { params: { from: 15508229741, to: 15663750341} , validateStatus: (status) => status === 422 });
    // console.log(response.status)
    // console.log('---------------')
    expect(response.status).toBe(422);
    expect(response.data.error).toBe("Resolution error");
  })


  it('400 lack of from', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/ape_twd', { params: { resolution: '3h', to: 15663750341} , validateStatus: (status) => status === 400 });
    // console.log(response.status)
    // console.log('---------------')
    expect(response.status).toBe(400);
    expect(response.data.error).toBe("Wrong parameter: from");
  })

  it('400 lack of to', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/ape_twd', { params: { resolution: '3h', from: 15508229741} , validateStatus: (status) => status === 400 });
    // console.log(response.status)
    // console.log('---------------')
    expect(response.status).toBe(400);
    expect(response.data.error).toBe("Wrong parameter: to");
  })

  it('422 from is larger than to', async () => {
    // 發送 HTTP GET 請求
    const response = await axios.get('https://api.bitopro.com/v3/trading-history/ape_twd', { params: { resolution: '3h', from: 1570822974, to: 1566375034} , validateStatus: (status) => status === 422 });
    // console.log(response.status)
    // console.log('---------------')
    expect(response.status).toBe(422);
    expect(response.data.error).toBe("Wrong parameter: Parameter `From` need to be less or equal to `To`");
  })

});

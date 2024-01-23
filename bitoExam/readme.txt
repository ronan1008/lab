1. 第一題我是用 xmind 撰寫
2. 第二題，正常來說 keyword 可以放另外一隻檔案，在 import 進來，但因為這只是一個小程式，我就寫在一起，可能會稍微亂一點，請多包涵。
   我的 robot 環境是在 venv 底下使用，環境可能跟你的不同，另外，這個網站是 https，我是用本機的憑證去跑，如果你要跑，可能要更改變數路徑。
   或是你可以使用 code review 或是 看 robot framework 的 report。
   我從公司離職了，我沒有 slack 可以使用，那一段是 pseudo code
   google sheet 那部分，要使用 google cloud sheet api，有點麻煩，我 gcp 沒那麼熟練，這部分我沒做。
3. 第三題在 question3&4 folder
4. 第四題，我跑 jest 的時候，有發現你們的規格問題，你可以嘗試跑我的 test，會出現3個錯誤。題目說只要20個以上，剩下 case 我就不寫了。
    a. resolution 帶入 1m 的時候，會回應 4xx，但是規格上有寫 1m 可以用。
    b. 規格上 data type 都是 string，但實際回傳的 大部分不是 string，我猜是你們文件沒有更新
    c. 理論上 response 的 timestamp 應該要介於 from 與 to 之間，但是第一筆資料的 timestamp 可能會比 from 小，但我認為是你們設計問題，這點我不確定。

  ● trading-history pair › 200 usdt_twd resolution 1m

    AxiosError: Request failed with status code 422

      at settle (node_modules/axios/lib/core/settle.js:19:12)
      at IncomingMessage.handleStreamEnd (node_modules/axios/lib/adapters/http.js:589:11)

  ● trading-history pair › 200 bito_twd resolution 1d : check data type is legal

    expect(received).toBe(expected) // Object.is equality

    Expected: "string"
    Received: "number"

      44 |     expect(response.status).toBe(200);
      45 |     console.log(response.data.data[0])
    > 46 |     expect(typeof response.data.data[0]['timestamp']).toBe("string")
         |                                                       ^

      at Object.toBe (question4.test.js:46:55)

  ● trading-history pair › 200 btc_twd check timestamp between from and to

    expect(received).toBeGreaterThanOrEqual(expected)

    Expected: >= 1550822974
    Received:    1550815200

      64 |       console.log(i, item)
      65 |       expect(item['timestamp'] / 1000).toBeLessThanOrEqual(1566375034)
    > 66 |       expect(item['timestamp'] / 1000).toBeGreaterThanOrEqual(1550822974)

      at toBeGreaterThanOrEqual (question4.test.js:66:40)
          at Array.forEach (<anonymous>)
      at Object.forEach (question4.test.js:63:10)

Test Suites: 1 failed, 1 total
Tests:       3 failed, 18 passed, 21 total
Snapshots:   0 total
Time:        2.783 s

5.

微服務（Microservices）是一種軟體架構風格，其中應用程式被切割成一組小型、自治、相互協作的服務。每個微服務都專注於執行單一業務功能，可以獨立開發、部署、擴展，並透過輕量的通訊機制進行互動。
假設有一個電子商務平台，原本的單一服務架構可能包含一個龐大的單一應用程式處理所有功能。透過微服務的轉換，我們可以將不同的業務功能切分為獨立的微服務：

    使用者服務：
        負責處理使用者註冊、登入、個人資料等相關功能。

    商品服務：
        管理商品資訊、庫存、價格等。

    訂單服務：
        負責處理訂單生成、支付、查詢等相關功能。

    付款服務：
        管理支付流程、金流整合等。

每個微服務都是一個獨立的單元，可以使用不同的技術堆疊和開發速度。它們透過 API 或其他通訊機制彼此協作，形成一個完整的電子商務平台。這樣的架構使得每個服務可以獨立擴展，並且容易進行更新和維護。

6. 我沒有測試分佈式系統的壓力測試經驗。但我倒是有使用 分布式 client 測試 系統的經驗。如果有機會面試，我當面說給你聽。
   或是參考，我在前公司 question6/小遊戲壓測報告，我使用多台 client 使用 python multi-thread 去測試 game server 的承載力。


    分佈式系統壓力測試計劃和場景：
    1. 目標設定：
        確定系統的預期使用者數量、交易量、或其他相關指標。
        考慮系統的承載能力和業務需求。
    2. 场景设计：
    正常流量场景：
        模擬系統在預期使用情況下的正常運作，確保基本功能正確且性能良好。

    峰值流量场景：
        將使用者數量增加至預期的最高峰值，觀察系統如何處理高流量。

    異常情境场景：
        引入意外的情境，例如服務中斷、資料庫錯誤，觀察系統是否能夠正確處理並恢復。

    持久性壓力测试：
        在長時間內持續高流量，檢測系統的穩定性和性能退化。

    3. 測試工具的選擇：
        使用壓力測試工具，如 Apache JMeter、Gatling、Locust，針對不同的系統和需求進行選擇。
    4. 執行測試：
        按照設計的場景，使用測試工具模擬實際使用情境，監控系統的反應時間、吞吐量、錯誤率等指標。
    5. 蒐集和分析結果：
        監控系統的基本資源，如 CPU 使用率、記憶體使用量、網路流量等。
        收集應用程式和服務的日誌，以追蹤異常情境和性能問題。
        使用測試結果和性能分析工具，識別系統的瓶頸和改進點。
    6. 調整和再測試：
        根據測試結果進行調整，可能需要優化程式碼、增加資源、調整配置等。
        進行迭代測試，確保系統在各種情境下都能夠正確、穩定地運行。
    蒐集和分析測試結果和 Log：
    1. 日誌收集：
        設定系統和應用程式以產生詳細的日誌，包括錯誤、警告、性能指標等。
        將日誌集中收集，使用日誌管理工具如 ELK Stack 或 Splunk。
    2. 測試結果收集：
        使用測試工具提供的報告和指標，記錄每個場景的性能數據。
        存儲測試結果於資料庫或檔案，以便後續分析。
    3. 分析和報告：
        使用性能分析工具進行深入的性能分析，識別瓶頸和問題。
        創建報告，包括性能指標、錯誤數量、反應時間分佈等。


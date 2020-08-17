const mongoose = require("mongoose")
const News = require("./models/news")
let mongoDbAtlas = "mongodb+srv://xzdzaorgtw:886229936810@xzdza.elxrf.mongodb.net/xzdza?retryWrites=true&w=majority"
//let mongoDB = "mongodb://localhost:27017/xzdza"

mongoose.connect(mongoDbAtlas, 
                    {
                        useNewUrlParser: true,
                        useUnifiedTopology: true,
                        useCreateIndex: true,
                        useFindAndModify: false
                    }
                )
News.deleteMany({})
    .then((items) => console.log(`Removed ${items.n} records`))
    .then(() => { 
        body = {
            title:"ECFA十年大限可免 RCEP警鐘響",
            description: "2010年時，由於9成石化產品未納入ECFA早收清單，台塑集團總裁王文淵表示，「很傷心」、「快要哭出來」；他擔心，也許短期影響不大，但眼見新加坡、泰國、韓國的乙烯產量追上台灣，長期將不利於台灣石化產業競爭力。10年後，面對石化業被拒於RCEP之外，王文淵則是「欲哭無淚」。今年5月台塑集團股東會期間，王文淵看到石化業挑戰嚴峻，除擔心中美貿易戰和新冠肺炎，更擔心RCEP今年底即將簽署，如此一來，台灣將面臨更多國際自由貿易關稅的不平等對待，不利台灣產業競爭。",
            type:"來年運勢",
            mark: true,
            order: 1,
            startTime:"2020-08-10 22:23:00",
            endTime:"2021-08-10 22:23:00"
        }
        return News.create(body)
    })
	.then( news => {
		console.log(`Created News: ${news.title}`)
    })
    .then(() => { 
        body = {
            title:"看好張震嶽、吳青峰拿獎",
            description: "據了解，中國打算先攻占金門、澎湖、馬祖等離島，並部屬海軍在台灣海峽的南北兩側，封鎖逃出的航路；另外，共軍也會再派軍艦到東部海岸協防美國第七艦隊，同時指示在台特務破壞軍事設備和關鍵設施，癱瘓所有網路和媒體。",
            type:"成果發表展",
            order: 1,
            startTime:"2019-08-10 22:23:00",
            endTime:"2019-08-10 22:23:00"
        }
        return News.create(body)
    })
	.then( news => {
		console.log(`Created News: ${news.title}`)
    })
    .then(() => { 
        body = {
            title:"父親節即將到來",
            description: "抖腳竟百益無一害？抖掉膝蓋痛、關節不卡、心臟還能變輕鬆",
            type:"最新消息",
            order: 4,
            startTime:"2019-08-10 22:23:00",
            endTime:"2019-08-10 22:23:00"
        }
        return News.create(body)
    })
	.then( news => {
		console.log(`Created News: ${news.title}`)
    })
    .then(() => { 
        body = {
            title:"樂購蝦皮股份有限公司",
            description: "小米預計在下週二（8/11）晚間發表小米10 系列的大尺寸版本，小米將這款新機中文命名為「小米10 至尊紀念版」，雷軍日前也透露這款新機也就是「小米10 Ultra」。近日在微博包括小米10 Ultra 的相機外觀設計、專用手機保護套陸續被洩露，小米 10 Ultra 將配備支持最高 120 倍變焦的四鏡頭主相機，同時 1 億 800 萬像素也將在主相機鏡頭配置中。",
            type:"最新消息",
            order: 3,
            startTime:"2020-08-10 22:23:00",
            endTime:"2020-08-10 22:23:00"
        }
        return News.create(body)
    })
	.then( news => {
		console.log(`Created News: ${news.title}`)
    })
    .then(() => { 
        body = {
            title:"欣亞購物網",
            description: "高雄市長補選結束，民進黨候選人陳其邁以67萬1804票當選高雄市長，儘管已經獲得了超過70%的得票率，但律師林智群指出，不管是陳其邁還是李眉蓁，他們的得票數都「遠低於韓國瑜」，直呼韓總不愧是高",
            type:"最新消息",
            order: 2,
            startTime:"2020-08-10 22:23:00",
            endTime:"2020-08-10 22:23:00"
        }
        return News.create(body)
    })
	.then( news => {
		console.log(`Created News: ${news.title}`)
    })
    .then(() => { 
        body = {
            title:"惡名昭彰股份有限公司",
            description: "林智群在臉書上發文指出，陳其邁在這次選舉中獲得了67萬票，比起韓國瑜2018年市長選舉的89萬票，甚或是在罷免投票中的94萬票，都遜色不少，直呼韓國瑜真的不簡單，不愧是「高雄之王」！藍、綠、白三位候選人都要敬他三分！",
            type:"最新消息",
            order: 1,
            startTime:"2020-08-10 22:23:00",
            endTime:"2020-08-10 22:23:00"
        }
        return News.create(body)
    })
	.then( news => {
		console.log(`Created News: ${news.title}`)
    })
    .then(() => { 
        body = {
            title:"PChome線上購物",
            description: "感謝您訂購PChome線上購物的優質產品 訂單編號：20200811588865 發票已經開立，發票號碼：DV40029080，電子發票不直接寄送，請至網站「顧客中心-查訂單」查看發票內容或索取正本。不愧是「高雄之王」！藍、綠、白三位候選人都要敬他三分！",
            type:"最新消息",
            order: 1,
            mark: true,
            startTime:"2020-08-10 22:23:00",
            endTime:"2020-08-10 22:23:00"
        }
        return News.create(body)
    })
	.then( news => {
		console.log(`Created News: ${news.title}`)
    })
    .then(() => { 
        body = {
            title:"PChome線上購物2",
            description: "感謝您訂購PChome線上購物的優質產品 訂單編號：20200811588865 發票已經開立，發票號碼：DV40029080，電子發票不直接寄送，請至網站「顧客中心-查訂單」查看發票內容或索取正本。不愧是「高雄之王」！藍、綠、白三位候選人都要敬他三分！",
            type:"最新消息",
            order: 1,
            mark: true,
            startTime:"2020-08-10 22:23:00",
            endTime:"2020-08-10 22:23:00"
        }
        return News.create(body)
    })
	.then( news => {
		console.log(`Created News: ${news.title}`)
    })
    .catch(error => {
        console.log(`Error saving news: ${error.message}`)
        next(error)
    })

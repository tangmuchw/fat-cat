const path = require("path");
const fs = require("fs");
const yargs = require("yargs/yargs");
const { hideBin } = require("yargs/helpers");

// --env=dev|prod
const argv = yargs(hideBin(process.argv)).argv;
const env = argv["env"] || "dev";
console.log("argv env=>", argv["env"]); // 例如：node script.js --name=John --age=

// 记得先创建 data 目录

const thanks = [
    // 感谢卡
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "thanks",
        typeName: "感谢卡",
        templateName: "改PPT之恩",
        cover: "thanks0001.png",
        salePrice: null,
        blessingWords: "深夜改PPT之恩，没齿难忘！",
        updatedAt: null,
    },
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "thanks",
        typeName: "感谢卡",
        templateName: "带饭之恩",
        cover: "thanks0002.png",
        salePrice: null,
        blessingWords:
            "从今以后，你的备注是【再生父母·食堂在逃天使·饿鬼拯救者】！请受我一拜！ORZ",
        updatedAt: null,
    },
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "thanks",
        typeName: "感谢卡",
        templateName: "职场新人致谢导师",
        cover: "thanks0003.png",
        salePrice: null,
        blessingWords:
            "新手村遇名师，何其有幸！您说的‘[导师金句]’已刻进职场DNA🧬",
        updatedAt: null,
    },
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "thanks",
        typeName: "感谢卡",
        templateName: "致疲惫时刻",
        cover: "thanks0004.png",
        salePrice: null,
        blessingWords: "连续肝了3天pre，没猝死就是胜利！奖励一顿炸鸡！",
        updatedAt: null,
    },
];

// 鼓励卡
const encourages = [
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "encourage",
        typeName: "鼓励卡",
        templateName: "反焦虑",
        cover: "encourage0001.png",
        salePrice: null,
        blessingWords: "怕什么？最坏的结果，不过是大器晚成。",
        updatedAt: null,
    },
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "encourage",
        typeName: "鼓励卡",
        templateName: "备考打气",
        cover: "encourage0002.png",
        salePrice: null,
        blessingWords: "凌晨的台灯和咖啡渍，都是未来讲给学弟妹的勋章故事✨",
        updatedAt: null,
    },
];

// 夸夸卡
const praises = [
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "praise",
        typeName: "夸夸卡",
        templateName: "认证搞事业",
        cover: "praise0001.png",
        salePrice: null,
        blessingWords: "你认真搞事业的样子，自带主角光环！",
        updatedAt: null,
    },
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "praise",
        typeName: "夸夸卡",
        templateName: "朋友彩虹屁",
        cover: "praise0002.png",
        salePrice: null,
        blessingWords:
            "与君初相识，犹如故人归——原来上辈子我们就是互吹彩虹屁的搭档啊！",
        updatedAt: null,
    },
];

// 道歉卡
const sorrys = [
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "sorry",
        typeName: "道歉卡",
        templateName: "鸽了饭局",
        cover: "sorry0001.png",
        salePrice: null,
        blessingWords: "鸽了饭局，欠你一顿火锅+奶茶。",
        updatedAt: null,
    },
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "sorry",
        typeName: "道歉卡",
        templateName: "吵架和解",
        cover: "sorry0002.png",
        salePrice: null,
        blessingWords: "吵架时说反话的我，其实超怕你转身走掉…",
        updatedAt: null,
    },
];

// 拒绝卡
const rejects = [
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "reject",
        typeName: "拒绝卡",
        templateName: "你超优秀",
        cover: "reject0001.png",
        salePrice: null,
        blessingWords: "你超优秀，但我怕耽误你发展。",
        updatedAt: null,
    },
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "reject",
        typeName: "拒绝卡",
        templateName: "拒绝借钱",
        cover: "reject0002.png",
        salePrice: null,
        blessingWords:
            "我现在的经济状况：苍蝇飞过都得留下买路钱，实在薅不出羊毛了🐑",
        updatedAt: null,
    },
];

// 纪念卡
const souvenirs = [
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "souvenir",
        typeName: "纪念卡",
        templateName: "往返车票",
        cover: "souvenir0001.png",
        salePrice: null,
        blessingWords: "用一张车票换走学生证，从此故乡只有冬夏",
        updatedAt: null,
        status: "offline",
    },
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "souvenir",
        typeName: "纪念卡",
        templateName: "致青春",
        cover: "souvenir0002.png",
        salePrice: null,
        blessingWords:
            "愿你此去前程似锦，再无风雨兼程，归来仍是少年，眼中满是星辰。",
        updatedAt: null,
        status: "online",
        isHot: 1,
    },
];

// 自嘲卡
const selfMockery = [
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "selfMockery",
        typeName: "自嘲卡",
        templateName: "天选打工人工资篇",
        cover: "selfMockery0001.png",
        salePrice: null,
        blessingWords: "工资三千八，拿命往里搭",
        updatedAt: null,
        status: "offline",
    },
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "selfMockery",
        typeName: "自嘲卡",
        templateName: "天选打工人凌晨篇",
        cover: "selfMockery0002.png",
        salePrice: null,
        blessingWords: "凌晨四点，看到海棠花未眠",
        updatedAt: null,
        status: "online",
        isHot: 1,
    },
];

const embrace = [
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "embrace",
        typeName: "抱抱卡",
        templateName: "抱紧我",
        cover: "embrace0001.png",
        salePrice: null,
        blessingWords: "抱紧我，让心跳缝补风的缺口。",
        updatedAt: null,
        status: "online",
        isHot: 1,
    },
];

const generateTemplateCode = (list) => {
    return list.map((v, idx) => ({
        ...v,
        templateCode: `${v.type}${(idx + 1).toString().padStart(4, "0")}`,
    }));
};

const cards = [
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "thanks",
        typeName: "感谢卡",
        templateCode: "thanks0000",
        templateName: "万笺集",
        cover: null,
        salePrice: null,
        blessingWords: "千言万语汇成一句：谢谢！❤️",
        updatedAt: null,
    },
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "sorry",
        typeName: "道歉卡",
        templateCode: "sorry0000",
        templateName: "万笺集",
        cover: null,
        salePrice: null,
        blessingWords: "为我的不当言行向您郑重道歉！🙏",
        updatedAt: null,
    },
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "encourage",
        typeName: "鼓励卡",
        templateCode: "encourage0000",
        templateName: "万笺集",
        cover: null,
        salePrice: null,
        blessingWords: "关关难过关关过，前路漫漫亦灿灿！🔥",
        updatedAt: null,
    },
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "reject",
        typeName: "拒绝卡",
        templateCode: "reject0000",
        templateName: " 万笺集",
        cover: null,
        salePrice: null,
        blessingWords: "很抱歉这次帮不上忙，但真心祝愿一切顺利！🙏",
        updatedAt: null,
    },
    {
        categoryType: "emotionalPurpose",
        categoryTypeName: "情感目的",
        type: "praise",
        typeName: "夸夸卡",
        templateCode: "praise0000",
        templateName: "万笺集",
        cover: null,
        salePrice: null,
        blessingWords: "救命！这是什么神仙操作！慕了慕了～",
        updatedAt: null,
    },
    // 分割--以上为默认模板
    ...generateTemplateCode(thanks),
    ...generateTemplateCode(encourages),
    ...generateTemplateCode(praises),
    ...generateTemplateCode(sorrys),
    ...generateTemplateCode(rejects),
    ...generateTemplateCode(souvenirs),
    ...generateTemplateCode(selfMockery),
    ...generateTemplateCode(embrace),
];

// const formatDate = (date) => {
//     const year = date.getFullYear();
//     const month = String(date.getMonth() + 1).padStart(2, "0");
//     const day = String(date.getDate()).padStart(2, "0");
//     const hours = String(date.getHours()).padStart(2, "0");
//     const minutes = String(date.getMinutes()).padStart(2, "0");
//     const seconds = String(date.getSeconds()).padStart(2, "0");

//     return `${year}-${month}-${day}${hours}:${minutes}:${seconds}`;
// };

const nowAt = new Date();

const cloudUrlConfig = {
    dev: "cloud://cloud1-1gte9qf85ff03da4.636c-cloud1-1gte9qf85ff03da4-1358849543/images/cover/",
    prod: "cloud://cloud1-4gcgkweic0306525.636c-cloud1-4gcgkweic0306525-1360400413/images/cover/",
};

const fileNameConfig = {
    dev: "dev_database_cards",
    prod: "prod_database_cards",
};

const cloudUrl = cloudUrlConfig[env];
const fileName = fileNameConfig[env];

const updatedCards = cards.map((v, idx) => {
    const id = v.templateCode;
    return {
        // id: "202505191212120002",
        _id: id,
        id,
        ...v,
        status: v.status || "online",
        // createAt: { $date: "2025-05-19T12:12:12.221Z" },
        createAt: null,
        cover: v.cover ? `${cloudUrl}${v.cover}` : null,
        isHot: v.isHot || 0,
    };
});

const hotCards = updatedCards
    .filter(({ isHot }) => isHot === 1)
    .map(
        ({ typeName, templateName, blessingWords }) =>
            `${typeName}·${templateName}·${blessingWords}`
    );
// .join("\n");

console.log("=== 热门推荐 ===");
console.table(hotCards);
console.log("=== 热门推荐 ===");

try {
    console.log("=== database_cards 开始处理 ===");
    const filePath = path.join(__dirname, `${fileName}.json`);
    const writeStream = fs.createWriteStream(filePath);

    updatedCards.forEach((item) => {
        writeStream.write(JSON.stringify(item) + "\n");
    });
    writeStream.end();
    console.log(`=== 写入成功-环境 ${argv["env"]} ===`);
} catch (err) {
    console.log(`=== 写入失败-环境 ${argv["env"]} ===`);
}

// 执行: node ./bear-card/json/database_cards.js
// 执行: node ./bear-card/json/database_cards.js --env=prod

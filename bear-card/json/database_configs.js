const path = require("path");
const fs = require("fs");
const yargs = require("yargs/yargs");
const { hideBin } = require("yargs/helpers");
const { createDirSync } = require("./utils");
const { CARD_CATEGORY_TYPES } = require("./constants");

// --env=dev|prod
const argv = yargs(hideBin(process.argv)).argv;
const env = argv["env"] || "dev";
console.log(`=== database_configs.js argv env: ${env} ===`); // 例如：node script.js --name=John --age=

const configs = {
    _id: "2025-06-11_latest",
    noticeBar: {
        show: true,
        actionType: "goMsgBoard",
        content: "翻遍熊熊卡没找着~帮它贴寻卡启事？📮🐻🔍",
    },
    cardCategoryTypes: CARD_CATEGORY_TYPES,

    slogan: {
        title: "你的专属熊信使，心意一键派送",
        description: "告别难开口，熊熊心意卡 + 解忧愁",
    },

    // 展示于 首页-顶部导航栏- logo 右侧
    appName: "熊熊卡·高情商表达小帮手",
};

const DIR_PATH = path.join(__dirname, `configs`);

const fileName = `${env}_database_configs.json`;

const createConfigsJson = () => {
    console.log("=== database_configs 开始处理 ===");
    const filePath = `${DIR_PATH}/${fileName}`;
    const writeStream = fs.createWriteStream(filePath);

    writeStream.write(JSON.stringify(configs) + "\n");
    writeStream.end();
    console.log(`=== 写入成功-环境 ${env} ===`);
};

try {
    createDirSync(DIR_PATH);

    createConfigsJson();
} catch (err) {
    console.log(`=== 写入失败-环境 ${env} ===`, err);
}

// 执行: node ./bear-card/json/database_configs.js --env=dev
// 执行: node ./bear-card/json/database_configs.js --env=preprod
// 执行: node ./bear-card/json/database_configs.js --env=prod

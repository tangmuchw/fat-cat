const path = require("path");
const fs = require("fs");
const yargs = require("yargs/yargs");
const { hideBin } = require("yargs/helpers");
const { createDirSync } = require("./utils");
const moment = require("moment");

// --env=dev|prod
const argv = yargs(hideBin(process.argv)).argv;
const env = argv["env"] || "dev";
console.log(`=== database_sent_card_records.js argv env: ${env} ===`); // 例如：node script.js --name=John --age=

const nowAt = moment();
const dateStr = nowAt.format("YYYY-MM-DDTHH:mm:ss.SSSZ");
const nowAtObj = { $date: dateStr };

console.log(`=== 更新时间: ${nowAtObj.$date} ===`);
const record = {
    _id: "ed863e8268558a49036926de61dccad6",
    sentId: "testid",
    cardId: "task0001",
    cardNumber: "GMC4364250466631508",
    status: "created",
    recipientOpenid: null,
    senderOpenid: "o7TSC4siUlso9PNAN6PyKh7q79RE",
    receivedAt: null,
    sentAt: null,
    createAt: nowAtObj,
    expiredAt: null,
};

const DIR_PATH = path.join(__dirname, `sent-card-records`);

const fileName = `${env}-sent-card-records.json`;

const createConfigsJson = () => {
    console.log("=== database_sent_card_records 开始处理 ===");
    const filePath = `${DIR_PATH}/${fileName}`;
    const writeStream = fs.createWriteStream(filePath);

    writeStream.write(JSON.stringify(record) + "\n");
    writeStream.end();
    console.log(`=== 写入成功-环境 ${env} ===`);
};

try {
    createDirSync(DIR_PATH);

    createConfigsJson();
} catch (err) {
    console.log(`=== 写入失败-环境 ${env} ===`, err);
}

// 执行: node ./bear-card/json/database_sent_card_records.js --env=dev
// 执行: node ./bear-card/json/database_sent_card_records.js --env=preprod
// 执行: node ./bear-card/json/database_sent_card_records.js --env=prod

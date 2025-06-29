import path from "path";
import fs from "fs";
import yargs from "yargs";
import moment from "moment";
import { hideBin } from "yargs/helpers";
import { createDirSync, getDevCloudUrl, log } from "./utils";
import { getCardsFromBBearCardExcel } from "./parse-excel";

// --env=dev|prod
const argv: any = yargs(hideBin(process.argv)).argv;
const env: "dev" | "prod" = argv["env"] || "dev";
log(`database-cards 输出环境 env: ${env}`); // 例如：node script.js --name=John --age=

const cloudUrlConfig = {
    dev: getDevCloudUrl(),
    // preprod:
    //     "cloud://cloud1-4gcgkweic0306525.636c-cloud1-4gcgkweic0306525-1360400413/images/cover/",
    prod: "cloud://prod-env-3gb9vy5c3ca5a90c.7072-prod-env-3gb9vy5c3ca5a90c-1360400413/images/cover/",
};

const fileNameConfig = {
    dev: "dev-database-cards",
    prod: "prod-database-cards",
};

// const cardCoverRatios = ["562x375", "676x338"];

// !important
const cloudUrl = cloudUrlConfig[env];
const fileName = fileNameConfig[env];

const nowAt = moment();
const dateStr = nowAt.format("YYYY-MM-DDTHH:mm:ss.SSSZ");
const updatedAt = { $date: dateStr };

const getUpdatedCards = async () => {
    const cardsFromBBEarCardExcel = await getCardsFromBBearCardExcel();

    if (!cardsFromBBEarCardExcel) {
        log("获取数据失败");
        return [];
    }
    const nextCards = cardsFromBBEarCardExcel.map((v, idx) => {
        return {
            ...v,
            status: v.status || "online",
            createAt: null,
            updatedAt,
            cover: v.cover ? `${cloudUrl}${v.cover}` : null,
            // copywriting: v.copywriting || "永久有效 | 编号唯一",
        };
    });

    return nextCards;
};

const CARDS_DIR_PATH = path.join(__dirname, `output/cards`);

const createCardsJson = async () => {
    console.log("=== database-cards 开始处理 ===");
    const filePath = `${CARDS_DIR_PATH}/${fileName}.json`;
    const writeStream = fs.createWriteStream(filePath);

    const updatedCardsFromExcel = await getUpdatedCards();
    updatedCardsFromExcel.forEach((item) => {
        writeStream.write(JSON.stringify(item) + "\n");
    });
    writeStream.end();
    log(
        `=== database-cards 写入成功-环境 ${env}, 共 ${updatedCardsFromExcel.length} 条 ===`
    );
};

try {
    createDirSync(CARDS_DIR_PATH);
    createCardsJson();
} catch (err) {
    console.log(`=== 写入失败-环境 ${env} ===`);
}

// 执行: ts-node  ./bear-card/json/src/database-cards.ts --env=dev
// 执行: ts-node  ./bear-card/json/src/database-cards.ts --env=prod

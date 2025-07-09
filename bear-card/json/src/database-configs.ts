import path from "path";
import fs from "fs";
import yargs from "yargs/yargs";
import { hideBin } from "yargs/helpers";
import { createDirSync, log } from "./utils";

// --env=dev|prod
const argv: any = yargs(hideBin(process.argv)).argv;
const env: "dev" | "prod" = argv["env"] || "dev";
log(`database-config.ts argv env: ${env}`); // 例如：node script.js --name=John --age=

const configs = {
    _id: "2025-06-11_latest",
    brandTitle: "不敢说的话熊熊来说",
    heroTitle: "让暖暖熊帮你传递心意，化解尴尬",
};

const DIR_PATH = path.join(__dirname, `output/configs`);

const fileName = `${env}-database-configs.json`;

const createConfigsJson = () => {
    log("database_configs 开始处理");
    const filePath = `${DIR_PATH}/${fileName}`;
    const writeStream = fs.createWriteStream(filePath);

    writeStream.write(JSON.stringify(configs) + "\n");
    writeStream.end();
    log(`写入成功-环境 ${env}`);
};

try {
    createDirSync(DIR_PATH);

    createConfigsJson();
} catch (err) {
    console.log(` 写入失败-环境 ${env} `, err);
}

// 执行: ts-node ./bear-card/json/src/database-configs.ts --env=dev
// 执行: ts-node ./bear-card/json/src/database-configs.ts --env=prod

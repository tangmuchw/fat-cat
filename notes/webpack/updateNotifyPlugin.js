import moment from 'moment';

class UpdateNotifyPlugin {
    constructor(options) { }

    apply(compiler) {
        compiler.hooks.emit.tapAsync('UpdateNotifyPlugin', (compilation, cb) => {
            const fileName = `/json/update_notify_plugin.json`;

            const fileContent = JSON.stringify({
                data: {
                    latest_release_at: moment().format('YYYYMMDDHHmmss'),
                },
            });

            compilation.assets[fileName] = {
                source: function () {
                    return fileContent;
                },
                size: function () {
                    return fileContent.length;
                },
            };

            cb();
        });
    }
}

export default UpdateNotifyPlugin;

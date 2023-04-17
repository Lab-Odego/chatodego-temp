const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
puppeteer.use(StealthPlugin());
const fs = require('fs');

const location = process.argv[2];

function timer(ms) {
    return new Promise(res => setTimeout(res, ms));
}

let path = [];
let queryString = "식당"

async function divide(page, leftTop, rightBottom, zoom) {
    const mid = [(leftTop[0] + rightBottom[0]) / 2, (leftTop[1] + rightBottom[1]) / 2];
    let result = false;
    while(!result) {
        try {
            await page.goto(`https://map.kakao.com/?urlX=${mid[0]}&urlY=${mid[1]}&urlLevel=${zoom}&q=${queryString}&currentBound=true`);
            result = true;
        }
        catch (err) {
            result = false;
        }
        await timer(2000);
    }

    let resultCnt = await page.evaluate(() => {
        return document.getElementById("info.search.place.cnt").innerText;
    });
    resultCnt = Number(resultCnt.replace(',', ''));

	// normal case
    if (resultCnt > 500) {
        path.push(1);
        await divide(page, leftTop, mid, zoom - 1);
        path.pop();
        path.push(2);
        await divide(page, [mid[0], leftTop[1]], [rightBottom[0], mid[1]], zoom - 1);
        path.pop();
        path.push(3);
        await divide(page, [leftTop[0], mid[1]], [mid[0], rightBottom[1]], zoom - 1);
        path.pop();
        path.push(4);
        await divide(page, mid, rightBottom, zoom - 1);
        path.pop();
    }
	// base case
    else if (resultCnt != 0) {
        await page.click('.option1')

        while(true) {
            await timer(1000);

            let places = [];
            // page가 있는지 체크 (result가 15개 이하)
            const isPageExist = await page.evaluate(() => {
                return document.getElementById("info.search.page").className == "pages";
            })

            // page가 없는 경우 -> 한 번만 실행
            if (!isPageExist) {
                places = await page.evaluate(() => {
                    let place = document.getElementsByClassName("PlaceItem clickArea");

                    let ret = [];
                    for (let i = 0; i < place.length; ++i) {
                        ret.push({
                            title : place[i].children[2].getElementsByClassName("link_name")[0].innerText,
                            category : place[i].children[2].getElementsByClassName("subcategory")[0].innerText,
                            address : place[i].children[4].children[1].children[0].innerText,
                            detailLink : place[i].children[4].children[5].getElementsByClassName("moreview")[0].href,
                        });
                    }
                    return ret;
                })

                for (let place of places) {
                    fs.appendFileSync("./places.json", JSON.stringify(place));
                    fs.appendFileSync("./places.json", ",\n\t");
                }
                break;
            }
            // page가 있는 경우
            else {
                // page개수를 구함
                const pageLength = await page.evaluate(() => {
                    let ret = 1;
                    for (; ret <= 5; ++ret) {
                        if (document.getElementById(`info.search.page.no${ret}`).className == "INACTIVE HIDDEN")
                            break;
                    }
                    return ret;
                })

                // page 클릭 후 crawl
                for (let pageNumber = 1; pageNumber < pageLength; ++pageNumber) {
                    await page.click(`#info\\.search\\.page\\.no${pageNumber}`);

                    await timer(1000);

                    places = await page.evaluate(() => {
                        let place = document.getElementsByClassName("PlaceItem clickArea");

                        let ret = [];
                        for (let i = 0; i < place.length; ++i) {
                            ret.push({
                                title : place[i].children[2].getElementsByClassName("link_name")[0].innerText,
                                category : place[i].children[2].getElementsByClassName("subcategory")[0].innerText,
                                address : place[i].children[4].children[1].children[0].innerText,
                                detailLink : place[i].children[4].children[5].getElementsByClassName("moreview")[0].href,
                            });
                        }
                        return ret;
                    })

                    for (let place of places) {
                        fs.appendFileSync("./places.json", JSON.stringify(place));
                        fs.appendFileSync("./places.json", ",\n\t");
                    }
                }
                

                // 더 page가 넘어가지는지 check
                const isEndOfResult = await page.evaluate(() => {
                    if (document.getElementById("info.search.page.next").className == "next disabled")
                        return true;
                    document.getElementById("info.search.page.next").click();
                    return false;
                })

                // 더 이상 못 넘어가는 경우 stop
                if (isEndOfResult)
                    break;
            }
        }
    }
}
 
async function doPuppeteer() {
    const options = {
        headless: false,
        ignoreHTTPSErrors: true,
	args : ['--window-size=1405,1130'],
    };

    const browser = await puppeteer.launch(options);
    
    const page = await browser.newPage();
    // Go to login page that redirect to userPage

    try {
        await divide(page, [-783715, 2422386], [1749487, -152403], 13);
    }
    catch (err) {
        console.log(err);
        console.log(path);
        
        browser.close();
        process.exit();
    }

    browser.close();
    process.exit();
}

doPuppeteer();


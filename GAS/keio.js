
//LINEからのイベントがdoPostにとんでくる
function doPost(e) {
  //とんできた情報を扱いやすいように変換している
  var json = e.postData.contents;
  var events = JSON.parse(json).events;

  var dat = sheet_userlist.getDataRange().getValues(); //受け取ったシートのデータを二次元配列に取得
  //とんできたイベントの種類を確認する
  events.forEach(function(event) {

    // ユーザーIDとユーザー名を取得
    var userId = event.source.userId;
    var nickname = getUserProfile(userId);
    var json  = UrlFetchApp.fetch("https://api.line.me/v2/bot/profile/" + userId, {"headers" : {"Authorization" : "Bearer " + channel_token}});
    var displayName = JSON.parse(json).displayName;
    //スプレッドシートに書き込む
    for(var i=1;i<dat.length;i++){
      if(dat[i][0] == userId){
        break;
      }
    }
    if(i==dat.length) {
      sheet_userlist.appendRow([userId, displayName]);
    }
    if(event.type == "message" && event.message.type == "text") {
      // if(event.message.type == "text"){
          // blank_room(e);
          var options = {
            "method" : "post",
            "headers" : {
              "Content-Type" : "application/json"
            },
            "payload" : JSON.stringify({text: event.message.text, replyToken: event.replyToken})
          };
          UrlFetchApp.fetch('FETCHURL', options);

          // var replyToken = event.replyToken;
          // var messageText = event.message.text;
          // replyMessage(messageText, replyToken);

          // circlefetch.replyMessage(messageText, replyToken);
          // fetchcircle(messageText, replyToken);
          
        // }
    }
    //もしイベントの種類がトークによるテキストメッセージだったら
    if(event.type == "postback") {
          var w_data = event.postback.data.split("&")[0].replace("data=","");//質問の内容を一時格納
          var w_item = event.postback.data.split("&")[1].replace("item=","");//回答を一時格納
          // 性別の回答がきたら
          if(w_data == "survey1") {
            sheet_userlist.getRange(i+1, 3).setValue(w_item);//スプレッドシートに性別の回答を入力
            survey_age(event);//入学年度の質問をリプライメッセージ送信
          }
          else if(w_data == "survey2") {
            sheet_userlist.getRange(i+1, 4).setValue(w_item);//スプレッドシートに性別の回答を入力
            survey_fac(event);//入学年度の質問をリプライメッセージ送信
          }
          else if(w_data == "survey3") {
            sheet_userlist.getRange(i+1, 5).setValue(w_item);//スプレッドシートに入学年度の回答を入力
            survey_end(event);//アンケートありがとうのリプライメッセージ送信
          }
        }
    else if(event.type == "follow") {
    console.log(event);
    var userId = event.source.userId;
    var data1 = SpreadsheetApp.openById("SHEELID');
    var last_row = data1.getLastRow();
    for(var i = last_row; i >= 1; i--) {
      if(data1.getRange(i,1).getValue() != '') {
        var j = i + 1;
        data1.getRange(j,1).setValue(nickname);
        data1.getRange(j,2).setValue(userId);
        data1.getDataRange().removeDuplicates([2])
        break;
      }
    }
    push_survey_new(event)
  }
 })
}
function fetchcircle(messageText, replyToken) {
  var url = "URL";
  var postData = {
    "messageText": messageText,
    "replyToken": replyToken
  };
  var options = {
    "method": "post",
    "payload": JSON.stringify(postData),
    "contentType": "application/json",
  };
  var response = UrlFetchApp.fetch(url, options);
  Logger.log(response.getContentText());
}
// profileを取得してくる関数（コピペでOK）
function getUserProfile(userId){ 
  var url = 'https://api.line.me/v2/bot/profile/' + userId;
  var userProfile = UrlFetchApp.fetch(url,{
    'headers': {
      'Authorization' :  'Bearer ' + channel_token,
    },
  })
  return JSON.parse(userProfile).displayName;
}
  

function survey_demogra() {
  var sheet = SpreadsheetApp.openById("SHEETID");
  var ss = sheet.getSheetByName('surveylist');
  var dat = ss.getDataRange().getValues(); //受け取ったシートのデータを二次元配列に取得
for(var i=1;i<dat.length;i++){
  push_survey(dat[i][0])
}
}

function push_survey_new(event){
var message = {
  "replyToken" : event.replyToken,
  'messages' : [
    {"type": "text","text" : "みなさんご自身にあった情報をお届けするため、性別・学部・学年を教えてください！\n\nまずは性別を選択してください。",
      "quickReply": {
          "items": [
            {
                "type": "action",
                "action": {
                    "type": "postback",
                    "label": "男性",
                    "data":"data=survey1&item=男性",
                    "displayText": "男性"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "postback",
                    "label": "女性",
                    "data":"data=survey1&item=女性",
                    "displayText": "女性"
                }
            }
          ]
        }}
  ]
    //★★★messages配信内容 end★★★
  };
//メッセージに添えなければならない情報
var options = {
  "method" : "post",
  "headers" : {
    "Content-Type" : "application/json",
    "Authorization" : "Bearer " + channel_token
  },
  "payload" : JSON.stringify(message)
};

//自動返信メッセージを送信する
UrlFetchApp.fetch(url, options);
}






function push_survey(userId){
  var url = "https://api.line.me/v2/bot/message/push";
  var headers = {
    "Content-Type" : "application/json; charset=UTF-8",
    'Authorization': 'Bearer ' + channel_token,
  };
  var postData = {
        "to" : userId,
  'messages' : [
    {"type": "text","text" : "こんにちは！\n学生団体Crichです。いつもありがとうございます😊 \n\n4月以降、みなさんご自身にあった情報をお届けするため、性別・学部・学年を教えてください！\n\nまずは性別を選択してください。",
      "quickReply": {
          "items": [
            {
                "type": "action",
                "action": {
                    "type": "postback",
                    "label": "男性",
                    "data":"data=survey1&item=男性",
                    "displayText": "男性"
                }
            },
            {
                "type": "action",
                "action": {
                    "type": "postback",
                    "label": "女性",
                    "data":"data=survey1&item=女性",
                    "displayText": "女性"
                }
            }
          ]
        }}
  ]

  }
   var options = {
        "method" : "post",
        "headers" : headers,
        "payload" : JSON.stringify(postData)
      };

      return UrlFetchApp.fetch(url, options);
}

function survey_age(event){
var message = {
  "replyToken" : event.replyToken,
  'messages' : [
    {"type": "text","text" : "入学年度を選択してください。",
    "quickReply": {
    "items": [
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "2023年度",
                "data":"data=survey2&item=2023年度",
                "displayText": "2023年度"
            }
        },
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "2022年度",
                "data":"data=survey2&item=2022年度",
                "displayText": "2022年度"
            }
        },
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "2021年度",
                "data":"data=survey2&item=2021年度",
                "displayText": "2021年度"
              }
        },
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "2020年度",
                "data":"data=survey2&item=2020年度",
                "displayText": "2020年度"
              }
        },
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "2019年度",
                "data":"data=survey2&item=2019年度",
                "displayText": "2019年度"
              }
        },
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "2018年度",
                "data":"data=survey2&item=2018年度",
                "displayText": "2018年度"
              }
        },
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "2017年度",
                "data":"data=survey2&item=2017年度",
                "displayText": "2017年度"
              }
        }
        ]
      }}
    ]
    //★★★messages配信内容 end★★★
  };
//メッセージに添えなければならない情報
var options = {
  "method" : "post",
  "headers" : {
    "Content-Type" : "application/json",
    "Authorization" : "Bearer " + channel_token
  },
  "payload" : JSON.stringify(message)
};

//自動返信メッセージを送信する
UrlFetchApp.fetch(url, options);
}
function survey_fac(event){
var message = {
  "replyToken" : event.replyToken,
  'messages' : [
    {"type": "text","text" : "所属学部を選択してください。",
    "quickReply": {
    "items": [
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "文学部",
                "data":"data=survey3&item=文学部",
                "displayText": "文学部"
            }
        },
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "経済学部",
                "data":"data=survey3&item=経済学部",
                "displayText": "経済学部"
              }
        },
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "法学部政治学科",
                "data":"data=survey3&item=法学部政治学科",
                "displayText": "法学部政治学科"
              }
        },
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "法学部法律学科",
                "data":"data=survey3&item=法学部法律学科",
                "displayText": "法学部法律学科"
              }
        },
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "商学部",
                "data":"data=survey3&item=商学部",
                "displayText": "商学部"
              }
        },
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "理工学部",
                "data":"data=survey3&item=理工学部",
                "displayText": "理工学部"
              }
        },
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "医学部",
                "data":"data=survey3&item=医学部",
                "displayText": "医学部"
              }
        },
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "総合政策学部",
                "data":"data=survey3&item=総合政策学部",
                "displayText": "総合政策学部"
              }
        },
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "環境情報学部",
                "data":"data=survey3&item=環境情報学部",
                "displayText": "環境情報学部"
              }
        },
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "薬学部",
                "data":"data=survey3&item=薬学部",
                "displayText": "薬学部"
              }
        },
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "看護医療学部",
                "data":"data=survey3&item=看護医療学部",
                "displayText": "看護医療学部"
              }
        },
        {
            "type": "action",
            "action": {
                "type": "postback",
                "label": "その他",
                "data":"data=survey3&item=その他",
                "displayText": "その他"
              }
        }
        ]
      }}
    ]
    //★★★messages配信内容 end★★★
};
//メッセージに添えなければならない情報
var options = {
  "method" : "post",
  "headers" : {
    "Content-Type" : "application/json",
    "Authorization" : "Bearer " + channel_token
  },
  "payload" : JSON.stringify(message)
};

//自動返信メッセージを送信する
UrlFetchApp.fetch(url, options);
}





function survey_end(event){
  var message = {
      "replyToken" : event.replyToken,
      //★★★messages配信内容★★★
      'messages' : [
        {"type": "text","text" : "アンケートのご協力ありがとうございました。"}
        ]
        //★★★messages配信内容 end★★★
    };
  //メッセージに添えなければならない情報
  var options = {
    "method" : "post",
    "headers" : {
      "Content-Type" : "application/json",
      "Authorization" : "Bearer " + channel_token
    },
    "payload" : JSON.stringify(message)
  };

  //自動返信メッセージを送信する
  UrlFetchApp.fetch(url, options);
}



function blank_room(e){
  var json = e.postData.contents
  var events = JSON.parse(json).events;
  var json = JSON.parse(e.postData.contents)
  var input = json.events[0].message;
    
  //とんできたイベントの種類を確認する
  events.forEach(function(event) {

    //もしイベントの種類がトークによるテキストメッセージだったら
          let mySheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("空き教室");
          const range = mySheet.getRange(2, 1, mySheet.getLastRow() - 1, mySheet.getLastColumn())
          const data = range.getValues() 
  
    for(let i = 0; i < data.length; i++){
      for(let j = 0; j < data[0].length; j++){
      if(input.text.match("^" + data[i][j] + "$")) {
        
          var cell = mySheet.getRange(i+2,j+1);
          var note = cell.getNotes();
          var message = {
                          "replyToken" : event.replyToken,
                          "messages" : [{"type": "text","text" : note[0][0]}]
                        };
          //メッセージに添えなければならない情報
          var options = {
            "method" : "post",
            "headers" : {
              "Content-Type" : "application/json",
              "Authorization" : "Bearer " + channel_token
            },
            "payload" : JSON.stringify(message)
          };

          //自動返信メッセージを送信する
          UrlFetchApp.fetch(url, options);
          }
      }
    }
  });
}


function findCircles(genre){
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("日程一覧");
  const genres = genre.split("/").concat(Array(3).fill("")).slice(0, 3);
  const data = sheet.getRange("A1:L" + sheet.getLastRow()).getValues();
  
  return data.reduce((acc, val) => {
    if (genres.every((g, i) => val[i + 7] === g)) {
      acc.push({ name: val[6], room: val[3], time: val[5], date: val[4], url: val[10], image: val[11], campus: val[0] });
    }
    return acc;
  }, []);
}

function sortByDate(circles, date){
  date = date.getDate();
  return circles.filter((item) => item.date.getDate() === date);
}

function checkUrlFetchQuota() {
 // var quotaRemaining = UrlFetchApp
  var quotaThreshold = 2000000000; // set your own threshold here
  
  if (true) {
    var message = "The remaining daily quota for URLFetch is ";
    var token = "TOKEN"; // set your own LINE Notify access token here
    var payload = {
      "to": "ID",
      "messages": [{
        "type": "text",
        "text": "Hey"
      }]
    };
    var options = {
      "method": "post",
      "headers": {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
      },
      "payload": JSON.stringify(payload)
    };
    var url = "https://api.line.me/v2/bot/message/push";
    UrlFetchApp.fetch(url, options);
  }
}

function replyMessage(message, replyToken) {
  const ACCESS_TOKEN = "TOKEN";
  var url = "https://api.line.me/v2/bot/message/reply";

  const date = new Date('2023-04-04');
  list = sortByDate(findCircles(message), date);

  bubbles = Array(Math.ceil(list.length / 12)).fill().map((_, i) =>
    list.slice(i * 12, (i + 1) * 12)
  );

  temps = [];

  for(let message of bubbles){
    var circles = {
      "type": "carousel",
      "contents": []
    };
    for(let i of message){
      var content = {
        "type": "bubble",
        "body": {
          "type": "box",
          "layout": "vertical",
          "contents": [
            {
              "type": "text",
              "text": String(i["name"]),
              "weight": "bold",
              "size": "xl",
              "wrap": true
            },
            {
              "type": "box",
              "layout": "vertical",
              "margin": "lg",
              "spacing": "sm",
              "contents": [
                {
                  "type": "box",
                  "layout": "baseline",
                  "spacing": "sm",
                  "contents": [
                    {
                      "type": "text",
                      "text": "教室",
                      "color": "#aaaaaa",
                      "size": "sm",
                      "flex": 1
                    },
                    {
                      "type": "text",
                      "text": String(i["room"]),
                      "wrap": true,
                      "color": "#666666",
                      "size": "sm",
                      "flex": 5
                    }
                  ]
                },
                {
                  "type": "box",
                  "layout": "baseline",
                  "spacing": "sm",
                  "contents": [
                    {
                      "type": "text",
                      "text": "時間",
                      "color": "#aaaaaa",
                      "size": "sm",
                      "flex": 1
                    },
                    {
                      "type": "text",
                      "text": String(i["time"]),
                      "wrap": true,
                      "color": "#666666",
                      "size": "sm",
                      "flex": 5
                    }
                  ]
                }
              ]
            }
          ]
        }
      }

      if(i["campus"] == "日吉"){
        content.footer = {
          "type": "box",
          "layout": "vertical",
          "spacing": "sm",
          "contents": [
            {
              "type": "box",
              "layout": "vertical",
              "spacing": "sm",
              "contents":[
                {
                  "type": "button",
                  "style": "secondary",
                  "action": {
                    "type": "message",
                    "label": "教室への行き方",
                    "text": String(i["room"])
                  }
                }
              ],
              "paddingTop": "sm"
            }
          ]
        }
      }

      if(!(i["url"] == "")){
        try{
          content.footer.contents.unshift({
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents":[
              {
                "type": "button",
                "style": "primary",
                "action": {
                  "type": "uri",
                  "label": "Crich Webでもっと見る",
                  "uri": i["url"]
                }
              }
            ]
          })
        }
        catch{
          content.footer = {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents":[
                  {
                    "type": "button",
                    "style": "primary",
                    "action": {
                      "type": "uri",
                      "label": "Crich Webでもっと見る",
                      "uri": i["url"]
                    }
                  }
                ],
                "paddingTop": "sm"
              }
            ]
          }
        }
      }

      if(!(i["image"] == "")){
        content.hero = {
          "type": "image",
          "size": "full",
          "aspectRatio": "20:13",
          "aspectMode": "cover",
          "url": i["image"]
        }
      }

      if(circles["contents"].length < 12){
        circles["contents"].push(content);
      }
      else{
        break;
      }
    }
    var temp = {
      "type": "flex",
      "altText": "サークル情報を送信しました。",
      "contents": circles
    };
    temps.push(temp);
  }

  if(temps.length == 0){
    temps = [
      {
        "type": "text",
        "text": "本日の出展サークルはありません！"
      }
    ];
  }

  var headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + ACCESS_TOKEN
  };
  var data = {
    "replyToken": replyToken,
    "messages": temps
  };
  var options = {
    "method": "post",
    "headers": headers,
    "payload": JSON.stringify(data),
    "muteHttpExceptions": true
  };

  try{
    const res = UrlFetchApp.fetch(url, options);
  }
  catch(error){
    console.log(error);
  }
}


import React, { useEffect } from 'react';
import Axios from 'axios';
import { useDispatch, useSelector } from 'react-redux';
import { saveMessage } from '../_actions/message_actions';
import Message from './Sections/Message';
import { List, Avatar } from 'antd';
import Card from "./Sections/Card";

/**************************************************************************************************************************************/
/**************************************** eventquery => 처음 채팅 소개 부분(사용자 입력 x) **********************************************/
/**************************************** textquery => 챗봇과 사용자 채팅 부분(사용자 입력 o) ********************************************/
/**************************************************************************************************************************************/

function Chatbot() {
    const dispatch = useDispatch();
    const messagesFromRedux = useSelector(state => state.message.messages)

    useEffect(() => { //event Query의 events 값 불러오면 event Query로 작동함
        eventQuery('IntroduceMyWebsite') //event Query 값 불러옴
    }, [])


    const textQuery = async (text) => { //서버에 request 보내기

        //  보낸 메시지 관리   
        let conversation = {
            who: 'user',
            content: {
                text: {
                    text: text
                }
            }
        }

        dispatch(saveMessage(conversation))
        // console.log('text I sent', conversation)

        // 챗봇이 보낸 메세지 관리
        const textQueryVariables = {
            text
        }
        try {
            //textquery에 request 보내기
            //const response = await Axios.post('/백엔드 경로, textQueryVariables)

            for (let content of response.data.fulfillmentMessages) {

                conversation = {
                    who: 'bot',
                    content: content
                }

                dispatch(saveMessage(conversation))
            }


        } catch (error) {
            conversation = {
                who: 'bot',
                content: {
                    text: {
                        text: " 죄송합니다. 오류가 발생했어요. "
                    }
                }
            }

            dispatch(saveMessage(conversation))


        }

    }


    const eventQuery = async (event) => {

        // We need to take care of the message Chatbot sent 
        const eventQueryVariables = {
            event
        }
        try {
            //I will send request to the textQuery ROUTE 
            const response = await Axios.post('/api/dialogflow/eventQuery', eventQueryVariables)
            for (let content of response.data.fulfillmentMessages) {

                let conversation = {
                    who: 'bot',
                    content: content
                }

                dispatch(saveMessage(conversation))
            }


        } catch (error) {
            let conversation = {
                who: 'bot',
                content: {
                    text: {
                        text: " Error just occured, please check the problem"
                    }
                }
            }
            dispatch(saveMessage(conversation))
        }

    }


    const keyPressHandler = (e) => {
        if (e.key === "Enter") {

            if (!e.target.value) { //입력칸이 비었을 경우
                return alert('내용을 입력해 주세요.')
            }

            //입력받으면 입력받은 내용 textquery로 전달
            textQuery(e.target.value)


            e.target.value = "";
        }
    }

    const renderCards = (cards) => {
        return cards.map((card,i) => <Card key={i} cardInfo={card.structValue} />)
    }


    const renderOneMessage = (message, i) => {
        console.log('message', message)

        // we need to give some condition here to separate message kinds 

        // template for normal text 
        if (message.content && message.content.text && message.content.text.text) {
            return <Message key={i} who={message.who} text={message.content.text.text} />
        } else if (message.content && message.content.payload.fields.card) {

            const AvatarSrc = message.who === 'bot' ? <img src={'bot_avatar.png'} alt='bot_avatar' style={{width: '32px', height: '32px'}} /> : <img src={'user_avatar.png'} alt='user_avatar' style={{width: '32px', height: '32px'}} />
            return <div>
                <List.Item style={{ padding: '1rem' }}>
                    <List.Item.Meta
                        avatar={<Avatar icon={AvatarSrc} />}
                        title={message.who}
                        description={renderCards(message.content.payload.fields.card.listValue.values)}
                    />
                </List.Item>
            </div>
        }

        // template for card message 

    }

    const renderMessage = (returnedMessages) => {

        if (returnedMessages) {
            return returnedMessages.map((message, i) => {
                return renderOneMessage(message, i);
            })
        } else {
            return null;
        }
    }


    return (
        // 채팅 상자
        <div style={{
            height: 600, width: 700,
            border: '3px solid black', borderRadius: '7px'
        }}>
            <div style={{ height: 544, width: '100%', overflow: 'auto' }}>


                {renderMessage(messagesFromRedux)}

            </div>
            <input
                style={{
                    margin: 0, width: '100%', height: 50,
                    borderRadius: '4px', padding: '5px', fontSize: '1rem'
                }}
                placeholder="Send a message..."
                onKeyPress={keyPressHandler} //keypresshandler
                type="text"
            />

        </div>
    )
}

export default Chatbot;

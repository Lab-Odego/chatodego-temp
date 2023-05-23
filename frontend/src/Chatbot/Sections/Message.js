import React from 'react'
import { List, Avatar } from 'antd';

function Message(props) {

    const AvatarSrc = props.who === 'bot' ? <img src={'bot_avatar.png'} alt='bot_avatar' style={{width: '32px', height: '32px'}} /> : <img src={'user_avatar.png'} alt='user_avatar' style={{width: '32px', height: '32px'}} />

    return (
        <List.Item style={{ padding: '1rem' }}>
            <List.Item.Meta
                avatar={<Avatar icon={AvatarSrc} />}
                title={props.who}
                description={props.text}
            />
        </List.Item>
    )
}

export default Message

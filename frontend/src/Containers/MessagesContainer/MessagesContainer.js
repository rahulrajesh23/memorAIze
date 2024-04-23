import React from 'react';
import { Loader } from '../../Components/Loader';

import styles from './MessagesContainer.module.css';

export function MessagesContainer(props) {
    const {
        messages = [],
        showLoader = false,
    } = props
    return (
        <div className={styles.messagesContainer}>
                {messages.map((message, index) => {
                    if(message) {
                        if(message.type == "question") {
                            return (
                                <div key={index} className={`${styles.message} ${styles.user}`}>
                                    <strong>Question:</strong> {message.question}
                                    <p><strong>Documents:</strong> 
                                        {
                                            message.docUrls && message.docUrls.map((documentUrl, msgIndex) => (
                                                <p key={msgIndex}> {documentUrl}</p>
                                            ))
                                        }
                                    </p>
                                </div>
                            )
                        }
                        else if (message.type == "response" && Array.isArray(message.facts)) {

                            return (
                                <div key={index} className={`${styles.message} ${styles.agent}`}>
                                    <strong>Response:</strong>
                                    {
                                        message.facts.map((fact, factIndex) => (
                                            <p key={factIndex}> {fact}</p>
                                        ))
                                    } 
                                </div>
                            )
                        }
                    }
                })}

                {showLoader && <Loader /> }
                
            </div>
    );
}

export default MessagesContainer;

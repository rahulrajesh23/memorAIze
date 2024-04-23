import React, { useState, useEffect, useRef } from 'react';
import { SubmitButton } from '../../Components/SubmitButton';
import { MultiCreateAbleSelect } from '../../Components/MultiCreateAbleSelect';
import { MessagesContainer } from '../MessagesContainer/';
import styles from './ChatScreen.module.css';
import { submitQuestionAndDocuments, getQuestionAndFacts } from '../../APIs';


function isValidUrl(url) {
    // const regex = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})(:[0-9]+)?(\/[\w \.-]*)*\/?(\.txt)?$/;
    const regex = /^https?:\/\/(?!((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(www\.)?[\da-z\.-]+\.[a-z\.]{2,6}(\/[\w\.-]*)*\/?(\.txt)?$/

    return regex.test(url);
}
const initialOptions = [
    { value: "https://storage.googleapis.com/cleric-assignment-call-logs/call_log_20240314_104111.txt", label: "https://storage.googleapis.com/cleric-assignment-call-logs/call_log_20240314_104111.txt" },
    { value: "https://storage.googleapis.com/cleric-assignment-call-logs/call_log_20240315_104111.txt", label: "https://storage.googleapis.com/cleric-assignment-call-logs/call_log_20240315_104111.txt" },
    { value: "https://storage.googleapis.com/cleric-assignment-call-logs/call_log_20240316_104111.txt", label: "https://storage.googleapis.com/cleric-assignment-call-logs/call_log_20240316_104111.txt" }
];

export function ChatScreen() {
    const [messages, setMessages] = useState([]);
    const [question, setQuestion] = useState('');
    const [waitingForResponse, setResponseState] = useState(false)
    const [options, setOptions] = useState(initialOptions);
    const [selectedOptions, setSelectedOptions] = useState([])
    const [selectedUrls, setSelectedUrls] = useState([])
    const [isInputFocused, setIsFocused] = useState(false)
    const questionInputRef = useRef(null);
    const questionRef = useRef(question)
    const selectedDocsRef = useRef(selectedUrls)
    let intervalID = null
    
    useEffect(() => {
        questionRef.current = question;
        selectedDocsRef.current = selectedUrls; 
    });

    useEffect(() => {
        // Listening for keydown so that I can trigger the Send Action
        window.addEventListener('keydown', handleKeyPress);

        return () => {
            // Clearing Interval and Keyboard listener
            clearInterval(intervalID)
            window.removeEventListener('keydown', handleKeyPress);
        };
    }, []); // Runs only on mount and unmount

    const updateMessagesFromResponse = () => {
        getQuestionAndFacts().then(response => {
            
            setMessages(currentMessages => {

                // Access the last question asked by the user
                const lastMessage = currentMessages.length > 0 ? currentMessages[currentMessages.length - 1] : null;

                // if The response recieved is for the last question (handling just in case), only then display the response
                if (response.status === "done" && lastMessage && lastMessage.question  && lastMessage.question === response.question) {

                    // Stop polling for response
                    clearInterval(intervalID);
                    setResponseState(false);

                    return [...currentMessages, {
                        question: response.question,
                        facts: response.facts,
                        type: "response"
                    }];
                }
                return currentMessages; // Return current state if no updates are necessary
            });
        }).catch(error => {
            console.error("Failed to get question and facts:", error);
        });
    };

    // Checks for messages at a certain interval if it is expecting a message
    const pollForResponse = () => {
        clearInterval(intervalID)
        intervalID = setInterval(updateMessagesFromResponse, 5000)
    }

    useEffect(() => {
        console.log(`The waitingForResponse has updated to: ${waitingForResponse}`);
        // Poll for response if we are expecting one
        if(waitingForResponse) {
            clearInterval(intervalID)
            pollForResponse()
        }      
        return () => {
            clearInterval(intervalID)
        };
    }, [waitingForResponse]);

    const  handleKeyPress = (event) => {
        if (event && event.key === 'Enter') {

            // Triggering Submit on Key press except if the the user is interacting with the multi select dropdown
            if(event.target && event.target.nodeName != "INPUT" ||  event.target == questionInputRef.current) {
                console.log(event, questionInputRef.current);
                console.log(question)
                handleSendMessage()
            }        
        }
    }

    const handleSendMessage = () => {
        const currentQuestion = questionRef.current
        const docUrls = selectedDocsRef.current

        // Check if we have a question and call log docuument paths
        if (!currentQuestion.trim() || !docUrls.length) return;

        setMessages(currentMessages => [
            ...currentMessages,
            {
                question: currentQuestion,
                docUrls: docUrls,
                type: 'question'
            }
        ]);

        submitQuestionAndDocuments(currentQuestion, docUrls);
        
        // Set a state to indicate that we are waiting for a response
        setResponseState(true); 

        // Clearing the input fields
        setQuestion('');
        setSelectedUrls([])
        setSelectedOptions([])
    };

    return (
        <div className={styles.chatContainer}>
            <div className={styles.bannerContainer}>
                <p>
                    Transcript AI
                </p>
            </div>

            <MessagesContainer messages={messages} showLoader={waitingForResponse}/>

            <div className={styles.chatActionContainer}>
                <div className={styles.formContainer}>
                    <div className={`${styles.questionContainer} ${isInputFocused && styles.focus || ''}`}>
                        <input
                            ref={questionInputRef}
                            type="text"
                            placeholder="Type your question here..."
                            className={styles.questionInput}
                            value={question}
                            onChange={(e) => setQuestion(e.target.value)}
                            onFocus={() => setIsFocused(true)}
                            onBlur={() => setIsFocused(false)}
                        />
                    </div>
                    <div className={styles.linksContainer}>
                        <MultiCreateAbleSelect
                            value={selectedOptions}
                            onChange={(selectedOptions, actionMeta) => {
                                if(actionMeta.action == 'clear') {
                                    // If all selected values are removed
                                    setSelectedUrls([])
                                    setSelectedOptions([])
                                }
                                else if (actionMeta.action === 'remove-value' || actionMeta.action === 'pop-value' && actionMeta.removedValue && actionMeta.removedValue.value) {
                                    // If a selected value is removed
                                    console.log('Removed value:', actionMeta.removedValue);
                                    setSelectedUrls(currentSelectedOptions => currentSelectedOptions.filter(item => item !== actionMeta.removedValue.value))
                                    setSelectedOptions(selectedOptions)
                                } else if (Array.isArray(selectedOptions) && selectedOptions.length > 0) {
                                    // Adding new document only if URL is valid
                                    const selectedUrl = selectedOptions[selectedOptions.length-1].value
                                    if(isValidUrl(selectedUrl)) {
                                        setSelectedOptions(selectedOptions)
                                        setSelectedUrls(currentUrls => [...currentUrls, selectedUrl])
                                    } else {
                                        // TODO: Handle url error
                                    }
                                }
                            }}
                            options={options}
                            onCreateOption={(inputValue) => {
                                if(isValidUrl(inputValue)) {
                                    const newOption = { value: inputValue, label: inputValue };
                                    setOptions(currentOptions => [...currentOptions, newOption]);
                                    setSelectedOptions(currentSelectedOptions => [...currentSelectedOptions, newOption]);
                                    setSelectedUrls(currentUrls => [...currentUrls, inputValue])
                                }}
                            }
                            placeholder="Type or select documents"
                        />
                    </div>
                </div>
                <div className={styles.submitBtnContainer}>
                    <SubmitButton
                        onClick={handleSendMessage}
                    />
                </div>
            </div>
        </div>
    );
}

export default ChatScreen;

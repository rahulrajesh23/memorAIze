import React, { useState } from 'react';
import styles from './SubmitButton.module.css';

export function SubmitButton(props) {
    const { onClick } = props
    const [isActiveOrHover, setActive] = useState(false)
    return (
        <button
            className={styles.sendButton}
            onClick={onClick}
            onFocus={() => setActive(true)}
            onBlur={() => setActive(false)}
            onMouseOver={() => setActive(true)}
            onMouseOut={() => setActive(false)}
        >
            {
                isActiveOrHover &&
                <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 16 16">
                    <path fill="#6ea9d7" d="M15.964.686a.5.5 0 0 0-.65-.65L.767 5.855H.766l-.452.18a.5.5 0 0 0-.082.887l.41.26l.001.002l4.995 3.178l3.178 4.995l.002.002l.26.41a.5.5 0 0 0 .886-.083zm-1.833 1.89L6.637 10.07l-.215-.338a.5.5 0 0 0-.154-.154l-.338-.215l7.494-7.494l1.178-.471z"></path>
                </svg>
                ||
                <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 16 16">
                    <path fill="#c9dff0" d="M15.964.686a.5.5 0 0 0-.65-.65L.767 5.855H.766l-.452.18a.5.5 0 0 0-.082.887l.41.26l.001.002l4.995 3.178l3.178 4.995l.002.002l.26.41a.5.5 0 0 0 .886-.083zm-1.833 1.89L6.637 10.07l-.215-.338a.5.5 0 0 0-.154-.154l-.338-.215l7.494-7.494l1.178-.471z"></path>
                </svg>
            }
        </button>
    );
}

export default SubmitButton;

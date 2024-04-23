import React from 'react';
import { ThreeDots } from 'react-loader-spinner'

import styles from './Loader.module.css';

export function Loader(props) {

    return (
        <div className={styles.loaderContainer}>
            <ThreeDots
            visible={true}
            height="20"
            width="20"
            color="#4fa94d"
            radius="9"
            ariaLabel="three-dots-loading"
            wrapperStyle={{}}
            wrapperClass=""
            />
        </div>
    );
}

export default Loader;
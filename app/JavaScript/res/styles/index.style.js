import { StyleSheet } from 'react-native';

export const colours = {
    black: '#1a1917',
    gray: '#888888',
    red: '#ff0000'
};

export default StyleSheet.create({
    safeArea: {
        flex: 1,
        backgroundColor: colours.black
    },
    exampleContainerLight: {
        backgroundColor: 'white'
    },
    slider: {
        marginTop: 15,
        overflow: 'visible' // for custom animations
    },
    sliderContentContainer: {
        paddingVertical: 10 // for custom animation
    }
});

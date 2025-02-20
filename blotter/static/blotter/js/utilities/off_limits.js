(() => {
    const header = 'OFF LIMITS! DO NOT ATTEMPT TO CONTINUE!';
    const message = `This setting is intended for developer users only. Caught in the act while trying to access this feature without any legal authorization will result in immediate action and reprimanded in accordance to the law of the Republic of the Philippines.`;
    const law = 'Republic Act No. 10175, known as the “Cybercrime Prevention Act of 2012”.';

    const headerStyle = 'font-family: "Segoe UI"; font-size: 64px; font-weight: bold; color: red; text-align: center; margin: 20px 0;';
    const lawStyle = 'font-family: "Segoe UI"; color: blue; font-size: 18px; font-weight: bold; text-align: center; margin: 20px 0;';
    const message_style = 'font-family: "Segoe UI"; font-size: 18px; color: black; text-align: justify; margin: 20px 0;';

    console.log(`%c${header}`, headerStyle);
    console.log(`%c${message}`, message_style);
    console.log(`%c${law}`, lawStyle);
})();

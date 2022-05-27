import math


class NumberToNepaliText():
    def __init__(self):
        pass

    def english_to_nepali(self, number):
        english_nepali_num = {'०': 0, '१': 1, '२': 2, '३': 3,
                              '४': 4, '५': 5, '६': 6, '७': 7, '८': 8, '९': 9}
        english_number = ""
        for s in str(number):
            english_number += str(english_nepali_num[s])
        return english_number

    def NumberToText(self, nepali_number):
        arrNumber = nepali_number.split('.')
        wholePart = int(self.english_to_nepali(arrNumber[0]))
        # print(number)

        numbersUptoHundred = [
            "शुन्य", "एक", "दुई", "तीन", "चार", "पाँच", "छ", "सात", "आठ", "नौ",
            "दश", "एघार", "बाह्र", "तेह्र", "चौध", "पन्ध्र", "सोह्र", "सत्र",
            "अठार", "उन्नाइस", "विस", "एक्काइस", "बाइस", "तेईस", "चौविस",
            "पच्चिस", "छब्बिस", "सत्ताइस", "अठ्ठाईस", "उनन्तिस", "तिस",
            "एकत्तिस", "बत्तिस", "तेत्तिस", "चौँतिस", "पैँतिस", "छत्तिस",
            "सैँतीस", "अठतीस", "उनन्चालीस", "चालीस", "एकचालीस", "बयालीस",
            "त्रियालीस", "चवालीस", "पैँतालीस", "छयालीस", "सच्चालीस", "अठचालीस",
            "उनन्चास", "पचास", "एकाउन्न", "बाउन्न", "त्रिपन्न", "चउन्न",
            "पचपन्न", "छपन्न", "सन्ताउन्न", "अन्ठाउन्न", "उनन्साठी", "साठी",
            "एकसट्ठी", "बयसट्ठी", "त्रिसट्ठी", "चौंसट्ठी", "पैंसट्ठी",
            "छयसट्ठी", "सतसट्ठी", "अठसट्ठी", "उनन्सत्तरी", "सत्तरी", "एकहत्तर",
            "बहत्तर", "त्रिहत्तर", "चौहत्तर", "पचहत्तर", "छयहत्तर", "सतहत्तर",
            "अठहत्तर", "उनासी", "असी", "एकासी", "बयासी", "त्रियासी", "चौरासी",
            "पचासी", "छयासी", "सतासी", "अठासी", "उनान्नब्बे", "नब्बे",
            "एकान्नब्बे", "बयानब्बे", "त्रियान्नब्बे", "चौरान्नब्बे",
            "पन्चानब्बे", "छयान्नब्बे", "सन्तान्नब्बे", "अन्ठान्नब्बे",
            "उनान्सय", "सय"]
        powers = ["हजार ", "लाख", "करोड", "अर्ब", "खर्ब"]
        # wordNumber = "रू. "
        wordNumber = ""
        # print(wholePart)
        while wholePart > 99:
            wholeNumberIntoCharArray = [s for s in str(wholePart)]
            # print(wholeNumberIntoCharArray)
            if len(wholeNumberIntoCharArray) < 4:
                hundredNumber = int(math.floor(float(wholePart / 100)))
                # print(hundredNumber)
                wordNumber += numbersUptoHundred[hundredNumber] + " "
                for_hundred = [s for s in str(wholePart / 100)]
                if len(for_hundred) > 1:
                    wordNumber += "सय" + " "
                wholePart = int(wholePart % 100)
            else:
                # Get index of power
                lengthOfNumber = len(wholeNumberIntoCharArray)
                isLengthOfNumberEven = lengthOfNumber % 2 == 0

                divisibleNumberInStringFormat = "1"

                if isLengthOfNumberEven:
                    powerIndex = (lengthOfNumber - 4) / 2
                    numberOfZerosInDivisibleNumber = lengthOfNumber - 1

                else:
                    numberOfZerosInDivisibleNumber = lengthOfNumber - 2
                    powerIndex = ((lengthOfNumber - 1) - 4) / 2
                for i in range(0, numberOfZerosInDivisibleNumber):
                    divisibleNumberInStringFormat += "0"

                divisibleNumber = int(divisibleNumberInStringFormat)
                tensNumber = int(math.floor(
                    float(wholePart / divisibleNumber)))
                powerIndex = int(powerIndex)
                wordNumber += str(numbersUptoHundred[tensNumber]) + \
                    " " + str(powers[powerIndex] + " ")
                wholePart = int(wholePart % divisibleNumber)
                # print(wholePart)

        if wholePart > 0:
            wordNumber += numbersUptoHundred[wholePart]

        if len(arrNumber) > 1:
            decimalPart = int(self.english_to_nepali(arrNumber[1]))

            wordNumber = self.appendPaisa(
                arrNumber, numbersUptoHundred, wordNumber)

        return wordNumber

    def appendPaisa(self, arrNumber, numbersUptoHundred, wordNumber):
        isNumberDecimal = len(arrNumber) == 2
        if isNumberDecimal:
            paisa = int(self.english_to_nepali(arrNumber[1]))
            if paisa > 0:
                #indexOfPaisa = paisa if paisa > 9 else (paisa * 10)
                # print(indexOfPaisa)
                wordNumber += numbersUptoHundred[paisa] + " " + "पैसा"
        return wordNumber

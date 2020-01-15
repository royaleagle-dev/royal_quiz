const option1 = document.querySelector('#option1');
                    console.log(option1.value)
                    const option2 = document.querySelector('#option2');
                    const option3 = document.querySelector('#option3');
                    const option4 = document.querySelector('#option4');
                    const btn = document.querySelector('#add');
                    const answer = document.querySelector('#answer');

                    //check whether the provided answer is in one of the options provided.
                    //if yes, retur true else return false.
                    function check(){
                        let checked;
                        let myArray = [];
                        myArray.push(option1.value);
                        myArray.push(option2.value);
                        myArray.push(option3.value);
                        myArray.push(option4.value);
                        for (let i = 0; i<myArray.length; i++){
                            let option = myArray[i];
                            if (option === answer.value){
                                checked = true;
                                break
                            }
                            else{
                                checked = false;
                                continue;
                            }   
                        }
                        return checked
                    }
                    
                    //when the button (btn) is clicked, run the check function, if true, allow form to be submitted,
                    //if false, prevent the form from submitting and highlight the answer field with a red background.
                    btn.onclick = function(event){
                        if (check() === false){
                            answer.style.backgroundColor = 'pink';
                            event.preventDefault();
                        }
                    }
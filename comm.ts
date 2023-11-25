function pr(input: any, type2?: number|string): void {
if (typeof type2 == "string") {
console.log(`///////////////////` ,type2, ' : ==>', input ,`///////////////////`);
} else {
console.log(typeof input, '==>', input);  
}
let _type = type2 ? type2 : 0;
let str = '';
if (_type > 0) {
for (let i = 0; i < 10; i++) str += _type.toString() + ' ';
console.log(`===========================    ${str}    =========================`);
}
}


export default pr;

// import pr from './comm'
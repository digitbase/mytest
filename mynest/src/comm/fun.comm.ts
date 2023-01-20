
export function pr(input: any, type2?: number): void {
  console.log(typeof input, '==>', input);
  let _type = type2 ? type2 : 0;
  let str = '';
  if (_type > 0) {
    for (let i = 0; i < 10; i++) str += _type.toString() + ' ';
    console.log(`===========================    ${str}    =========================`);
  }
}
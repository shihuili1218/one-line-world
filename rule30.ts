let r = 1n; for (let y = 0; y < 24; y++) { let row = ""; for (let b = 47; b >= 0; b--) row += (r >> BigInt(b) & 1n) ? "█" : " "; console.log(row); r = (r << 1n) ^ (r | (r >> 1n)); }

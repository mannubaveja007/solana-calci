use anchor_lang::prelude::*;

declare_id!("8MsFsFz1cPshextfGhHCgXStV7YudFCPZWje3dU4n24t");

#[program]
pub mod calci {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        msg!("Greetings from: {:?}", ctx.program_id);
        Ok(())
    }

    // Fixed: Arguments 'a' and 'b' should be passed directly to the function.
    // 'ctx.accounts' is for Solana Accounts (addresses), not data values.
    pub fn add(_ctx: Context<Add>, a: i64, b: i64) -> Result<()> {
        let result = a + b;
        msg!("Result: {}", result); // specific result message
        Ok(())
    }

    pub fn sub(_ctx: Context<Sub>, a: i64, b: i64) -> Result<()> {
        let result = a - b;
        msg!("Result: {}", result);
        Ok(())
    }

    pub fn mul(_ctx : Context<Mul> , a: i64 , b : i64) -> Result<()>{
        let result = a * b;
        msg!("Result : {}", result);
        Ok(())
    }

    pub fn div(_ctx : Context<Div> , a : i64 , b : i64) -> Result<()>{
        let result = a / b;
        msg!("Result : {}" , result);
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize {}

#[derive(Accounts)]
pub struct Add {}

#[derive(Accounts)]
pub struct Sub {}

#[derive(Accounts)]
pub struct Mul {}

#[derive(Accounts)]
pub struct Div {}
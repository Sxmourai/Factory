#![allow(unused_imports)]
use macroquad::prelude::*;
use ui::draw_ui;

mod ui;

#[macroquad::main("")]
async fn main() {
    loop {
        clear_background(BLACK);
        
        draw_ui();
        next_frame().await
    }
}
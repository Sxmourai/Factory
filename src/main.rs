#![allow(unused_mut)]
mod setup;
mod renderer;
mod player;
mod ui;
mod camera;
mod world;

use bevy::prelude::*;
use setup::SetupPlugin;

fn main() {
    App::new()
    .add_plugins(SetupPlugin)
    .run();
}
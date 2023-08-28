mod research;
mod machine;
use bevy::{utils::HashMap, prelude::*, window::PrimaryWindow};
use research::Research;

use crate::player::{Player, self};

use self::machine::{Machine, MachineType};
pub const TILE_SIZE: Vec2 = Vec2::new(50.0, 50.0);
#[derive(Resource)]
pub struct World {
    seed: u64,
    diff_world: HashMap<Transform, Machine>,
    research: Vec<(bool, Research)>,
}
impl World {
    pub fn new(seed: u64) -> Self {
        Self {
            seed,
            diff_world: HashMap::new(),
            research: Vec::new(), //TODO Initialize all researchs
        }
    }
    pub fn construct(pos: Transform, machine_type: MachineType) -> Result<(), BuildErr> {
        todo!()
    }
}

pub fn draw_world(_world: Res<World>,
    mut commands: Commands, 
    player: Query<(&Transform, With<Player>)>, 
    tiles: Query<(Entity, With<Tile>,Without<Player>)>,
    assets: Res<AssetServer>,
    primary_window: Query<&Window, With<PrimaryWindow>>) {
    for (entity, _, _) in &tiles {
        commands.entity(entity).despawn();
    }
    let player_pos = player.single().0.translation;
    let res = &primary_window.single().resolution;
    let (w,h) = (res.width(), res.height());
    
    let texture = assets.load("tile.png");
    for x in     (-TILE_SIZE.x as isize..=(w+TILE_SIZE.x*2.) as isize).step_by(TILE_SIZE.x as usize) {
        for y in (-TILE_SIZE.y as isize..=(h+TILE_SIZE.y*2.) as isize).step_by(TILE_SIZE.y as usize) {
            let mut x = x as f32;let mut y = y as f32;
            x += player_pos.x-w/2.;
            y += player_pos.y-h/2.;
            x -= x%TILE_SIZE.x;
            y -= y%TILE_SIZE.y;
            commands.spawn((SpriteBundle {
                sprite: Sprite {
                    custom_size: Some(TILE_SIZE),
                    ..default()
                },
                texture: texture.clone(),
                transform: Transform::from_translation(Vec3::new(x,y,0.0)),
                ..default()
            }, Block, Tile));
        }
    }
}

#[derive(Component)]
pub struct Block;
#[derive(Component)]
pub struct Tile;
pub enum BuildErr {
    SpaceIsNotEmpty
}
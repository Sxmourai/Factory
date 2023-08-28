use bevy::prelude::*;

use crate::player::Player;

#[derive(Resource)]
pub struct Money(pub f32);

#[derive(Component)]
pub struct MoneyText;

pub struct UIPlugin;
impl Plugin for UIPlugin {
    fn build(&self, app: &mut App) {
        app.add_systems(Startup, game_ui)
        ;
    }
}


pub fn game_ui(mut commands: Commands, assets: Res<AssetServer>) {
    commands.spawn((NodeBundle {
        style: Style {
            width: Val::Percent(80.0),
            height: Val::Percent(15.0),
            align_items: AlignItems::Center,
            padding: UiRect::all(Val::Px(10.0)),
            justify_content: JustifyContent::Center,
            top: Val::Percent(85.0),
            position_type: PositionType::Absolute,
            ..default()
        },
        ..default()
    }, Name::new("Hotbar"))).with_children(|commands| {
        commands.spawn(ButtonBundle {
            style: Style {
                width: Val::Px(64.0),
                height: Val::Px(64.0),
                ..default()
            },
            background_color: Color::BEIGE.into(),
            image: UiImage::new(assets.load("construct.png")),
            interaction: Interaction::Pressed,
            ..default()
        });
        commands.spawn(ButtonBundle {
            style: Style {
                width: Val::Px(64.0),
                height: Val::Px(64.0),
                ..default()
            },
            background_color: Color::BEIGE.into(),
            image: UiImage::new(assets.load("deconstruct.png")),
            interaction: Interaction::Pressed,
            ..default()
        });
    });

    commands.spawn((
        NodeBundle {
            style: Style {
                width: Val::Percent(100.0),
                height: Val::Percent(10.0),
                align_items: AlignItems::Center,
                padding: UiRect::all(Val::Px(10.0)),
                justify_content: JustifyContent::SpaceBetween,
                ..default()
            },
            background_color: Color::rgb(0.2, 0.2, 0.2).into(),
            ..default()
        },
        Name::new("Status bar")
    )).with_children(|commands| {
        commands.spawn((
            TextBundle {
                text: Text::from_section("Money", TextStyle { font_size: 16.0, ..default() }),
                ..default()
            },
            MoneyText
        ));
        commands.spawn(
            TextBundle {
                text: Text::from_section("Health", TextStyle { font_size: 16.0, ..default() }),
                ..default()
            }
        );
        commands.spawn(
            TextBundle {
                text: Text::from_section("Energy", TextStyle { font_size: 16.0, ..default() }),
                ..default()
            }
        );
    });
}

pub fn update_ui(
    mut texts: Query<&mut Text>, 
    player: Query<&Player>,
    mut interaction_query: Query<(
            &Interaction,
            &mut BackgroundColor,
            &mut BorderColor,
            &Children,),
        (Changed<Interaction>, With<Button>),>,) {
    for mut text in &mut texts {
        if text.sections[0].value.contains("Money") {
            text.sections[0].value = format!("Money: ${:?}", player.single().money);
        }
        else if text.sections[0].value.contains("Health") {
            text.sections[0].value = format!("Health: {:?}", player.single().health);
        }
        else if text.sections[0].value.contains("Energy") {
            text.sections[0].value = format!("Energy: {:?}", player.single().energy);
        }
    }
    
    for (interaction, mut color, mut border_color, children) in &mut interaction_query {
        match *interaction {
            Interaction::Pressed => {
            }
            _ => {}
        }
    }
}
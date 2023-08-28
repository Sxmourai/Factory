use bevy::prelude::*;

#[derive(Resource)]
pub struct Money(pub f32);

#[derive(Component)]
struct MoneyText;


pub fn game_ui(mut commands: Commands) {
    commands.spawn((
        NodeBundle {
            style: Style {
                width: Val::Percent(100.0),
                height: Val::Percent(100.0),
                align_items: AlignItems::Center,
                padding: UiRect::all(Val::Px(10.0)),
                ..default()
            },
            background_color: Color::BLUE.into(),
            ..default()
        },
        Name::new("UI Root")
    )).with_children(|commands| {
        commands.spawn((
            TextBundle {
                text: Text::from_section("Money", TextStyle { font_size: 32.0, ..default() }),
                ..default()
            },
            MoneyText
        ));
    });
}
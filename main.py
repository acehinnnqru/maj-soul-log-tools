import click
import logging

import cmds


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode")
def app(verbose):
    if verbose:
        click.secho("Enabling verbose mode\n", fg="yellow")
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


@app.command("st")
@click.option("--file", default="state.json", help="State file path")
def state(file):
    click.echo("cmd: state\n")
    logging.info(f"file: {file}")
    cmds.state(file)


@app.command("dl")
@click.option("--state_file", default="state.json", help="State file path")
@click.option("--profile", help="Profile directory path", required=True)
@click.option("--output", default="output", help="Logs directory path")
@click.option("--scripts", default="scripts", help="Scripts directory path")
@click.argument("log_id_or_data_file", nargs=1)
def download(state_file, profile, output, scripts, log_id_or_data_file):
    output_dir = output
    scripts_dir = scripts
    click.echo("cmd: download\n")
    if log_id_or_data_file.endswith(".csv"):
        click.echo(f"download all with {log_id_or_data_file}")
        cmds.download_all(output_dir, state_file, profile, scripts_dir, log_id_or_data_file)
    else:
        click.echo(f"download {log_id_or_data_file}")
        cmds.download_log(output_dir, state_file, profile, scripts_dir, log_id_or_data_file)


@app.command()
@click.option("--logs_dir", default="output/logs", help="Logs directory path")
@click.option("--output_dir", default="output", help="Output directory path")
@click.option("--diff", is_flag=True, help="Diff mode")
@click.option("--data", default="data.csv", help="Data file path (required in diff mode)")
def logs(logs_dir, output_dir, diff, data):
    click.echo("cmd: logs\n")
    cmds.logs(logs_dir, output_dir, diff, data)


@app.group('cal')
@click.option("--logs_dir", default="output/logs", help="Logs directory path")
@click.option("--output_dir", default="output", help="Output directory path")
@click.pass_context
def calculate(ctx, logs_dir, output_dir):
    click.echo("cmd: calculate")
    ctx.ensure_object(dict)
    ctx.obj["logs_dir"] = logs_dir
    ctx.obj["output_dir"] = output_dir


@calculate.command("longest_fail")
@click.pass_context
def longest_fail(ctx):
    click.echo("sub command: longest_fail\n")
    longest, users, _ = cmds.calculate_longest_fail(ctx.obj["logs_dir"], ctx.obj["output_dir"])
    click.secho(f"longest: {longest}, users: {users}", blink=True, bold=True, fg="green")


if __name__ == '__main__':
    app()
